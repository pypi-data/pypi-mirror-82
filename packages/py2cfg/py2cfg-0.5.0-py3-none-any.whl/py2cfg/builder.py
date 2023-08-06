#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Control flow graph builder.
"""

from typing import List, Optional
import ast  # type: ignore
from _ast import (
    Import,
    Break,
    AnnAssign,
    For,
    ImportFrom,
    Assign,
    AugAssign,
    Call,
    ClassDef,
    Compare,
    Expr,
    FunctionDef,
    If,
    Module,
    Return,
    stmt,
    While,
    Yield,
)  # type: ignore
from py2cfg.model import Block, Link, CFG, FuncBlock


def invert(node: Compare) -> Compare:
    """
    Invert the operation in an ast node object (get its negation).

    Args:
        node: An ast node object.

    Returns:
        An ast node object containing the inverse (negation) of the input node.
    """
    inverse = {
        ast.Eq: ast.NotEq,
        ast.NotEq: ast.Eq,
        ast.Lt: ast.GtE,
        ast.LtE: ast.Gt,
        ast.Gt: ast.LtE,
        ast.GtE: ast.Lt,
        ast.Is: ast.IsNot,
        ast.IsNot: ast.Is,
        ast.In: ast.NotIn,
        ast.NotIn: ast.In,
    }

    if isinstance(node, ast.Compare):
        op = type(node.ops[0])
        inverse_node = ast.Compare(
            left=node.left, ops=[inverse[op]()], comparators=node.comparators
        )
    elif isinstance(node, ast.NameConstant) and node.value in [True, False]:
        inverse_node = ast.NameConstant(value=not node.value)
    else:
        inverse_node = ast.UnaryOp(op=ast.Not(), operand=node)

    return inverse_node


def merge_exitcases(exit1: Optional[Compare], exit2: None) -> Optional[Compare]:
    """
    Merge the exitcases of two Links.

    Args:
        exit1: The exitcase of a Link object.
        exit2: Another exitcase to merge with exit1.

    Returns:
        The merged exitcases.
    """
    if exit1:
        if exit2:
            return ast.BoolOp(ast.And(), values=[exit1, exit2])
        return exit1
    return exit2


class CFGBuilder(ast.NodeVisitor):
    """
    Control flow graph builder.

    A control flow graph builder is an ast.NodeVisitor that can walk through
    a program's AST and iteratively build the corresponding CFG.
    """

    def __init__(self, short: bool = True) -> None:
        self.isShort = short
        self._callbuf: FuncBlock = []

    # ---------- CFG building methods ---------- #
    def build(
        self, name: str, tree: Module, asynchr: bool = False, entry_id: int = 0
    ) -> CFG:
        """
        Build a CFG from an AST.

        Args:
            name: The name of the CFG being built.
            tree: The root of the AST from which the CFG must be built.
            async: Boolean indicating whether the CFG being built represents an
                   asynchronous function or not. When the CFG of a Python
                   program is being built, it is considered like a synchronous
                   'main' function.
            entry_id: Value for the id of the entry block of the CFG.

        Returns:
            The CFG produced from the AST.
        """
        self.cfg = CFG(name, asynchr=asynchr, short=self.isShort)
        # Tracking of the current block while building the CFG.
        self.current_id = entry_id
        self.current_block = self.new_block()
        self.cfg.entryblock = self.current_block
        # Actual building of the CFG is done here.
        self.visit(tree)
        self.clean_cfg(self.cfg.entryblock)
        return self.cfg

    def build_from_src(self, name: str, src: str) -> CFG:
        """
        Build a CFG from some Python source code.

        Args:
            name: The name of the CFG being built.
            src: A string containing the source code to build the CFG from.

        Returns:
            The CFG produced from the source code.
        """
        tree = ast.parse(src, mode="exec")
        return self.build(name, tree)

    def build_from_file(self, name: str, filepath: str) -> CFG:
        """
        Build a CFG from some Python source file.

        Args:
            name: The name of the CFG being built.
            filepath: The path to the file containing the Python source code
                      to build the CFG from.

        Returns:
            The CFG produced from the source file.
        """
        with open(filepath, "r") as src_file:
            src = src_file.read()
            return self.build_from_src(name, src)

    # ---------- Graph management methods ---------- #
    def new_block(self) -> Block:
        """
        Create a new block with a new id.

        Returns:
            A Block object with a new unique id.
        """
        self.current_id += 1
        return Block(self.current_id)

    def new_func_block(self) -> FuncBlock:
        """
        Create a new function block with a new id.

        Returns:
            A FuncBlock object with a new unique id.
        """
        self.current_id += 1
        return FuncBlock(self.current_id)

    def add_statement(self, block: Block, statement: stmt) -> None:
        """
        Add a statement to a block.

        Args:
            block: A Block object to which a statement must be added.
            statement: An AST node representing the statement that must be
                       added to the current block.
        """
        block.statements.append(statement)

    def add_exit(
        self, block: Block, nextblock: Block, exitcase: Optional[Compare] = None
    ) -> None:
        """
        Add a new exit to a block.

        Args:
            block: A block to which an exit must be added.
            nextblock: The block to which control jumps from the new exit.
            exitcase: An AST node representing the 'case' (or condition)
                      leading to the exit from the block in the program.
        """
        newlink = Link(block, nextblock, exitcase)
        block.exits.append(newlink)
        nextblock.predecessors.append(newlink)

    def new_loopguard(self) -> Block:
        """
        Create a new block for a loop's guard if the current block is not
        empty. Links the current block to the new loop guard.

        Returns:
            The block to be used as new loop guard.
        """
        if self.current_block.is_empty() and len(self.current_block.exits) == 0:
            # If the current block is empty and has no exits, it is used as
            # entry block (condition test) for the loop.
            loopguard = self.current_block
        else:
            # Jump to a new block for the loop's guard if the current block
            # isn't empty or has exits.
            loopguard = self.new_block()
            self.add_exit(self.current_block, loopguard)

        return loopguard

    def new_classCFG(self, node: ClassDef, asynchr: bool = False) -> None:
        """
        Create a new sub-CFG for a class definition and add it to the
        class CFGs of the CFG being built.

        Args:
            node: The AST node containing the class definition.
            async: Boolean indicating whether the class for which the CFG is
                   being built is asynchronous or not.
        """
        self.current_id += 1
        # A new sub-CFG is created for the body of the class definition and
        # added to the class CFGs of the current CFG.
        class_body = ast.Module(body=node.body)
        class_builder = CFGBuilder(short=self.isShort)
        self.cfg.classcfgs[node.name] = class_builder.build(
            node.name, class_body, asynchr, self.current_id
        )
        self.current_id = class_builder.current_id + 1

    def new_functionCFG(self, node: FunctionDef, asynchr: bool = False) -> None:
        """
        Create a new sub-CFG for a function definition and add it to the
        function CFGs of the CFG being built.

        Args:
            node: The AST node containing the function definition.
            async: Boolean indicating whether the function for which the CFG is
                   being built is asynchronous or not.
        """
        self.current_id += 1
        # A new sub-CFG is created for the body of the function definition and
        # added to the function CFGs of the current CFG.
        func_body = ast.Module(body=node.body)
        func_builder = CFGBuilder(short=self.isShort)
        self.cfg.functioncfgs[node.name] = func_builder.build(
            node.name, func_body, asynchr, self.current_id
        )
        self.current_id = func_builder.current_id + 1

    def clean_cfg(self, block: Block, visited: List[Block] = []) -> None:
        """
        Remove the useless (empty) blocks from a CFG.

        Args:
            block: The block from which to start traversing the CFG to clean
                   it.
            visited: A list of blocks that already have been visited by
                     clean_cfg (recursive function).
        """
        # Don't visit blocks twice.
        if block in visited:
            return
        visited.append(block)

        # Empty blocks are removed from the CFG.
        if block.is_empty():
            for pred in block.predecessors:
                for exit in block.exits:
                    self.add_exit(
                        pred.source,
                        exit.target,
                        merge_exitcases(pred.exitcase, exit.exitcase),
                    )
                    # Check if the exit hasn't yet been removed from
                    # the predecessors of the target block.
                    if exit in exit.target.predecessors:
                        exit.target.predecessors.remove(exit)
                # Check if the predecessor hasn't yet been removed from
                # the exits of the source block.
                if pred in pred.source.exits:
                    pred.source.exits.remove(pred)

            block.predecessors = []
            for exit in block.exits:
                self.clean_cfg(exit.target, visited)
            block.exits = []
        else:
            for exit in block.exits:
                self.clean_cfg(exit.target, visited)

    # ---------- AST Node visitor methods ---------- #
    def visit_ClassDef(self, node: ClassDef) -> None:
        self.add_statement(self.current_block, node)
        self.new_classCFG(node, asynchr=False)

    def visit_Expr(self, node: Expr) -> None:
        self.add_statement(self.current_block, node)
        self.generic_visit(node)

    def visit_Call(self, node: Call) -> None:
        def visit_func(node):
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Attribute):
                # Recursion on series of calls to attributes.
                func_name = visit_func(node.value)
                func_name += "." + node.attr
                return func_name
            elif isinstance(node, ast.Subscript):
                return node.value.id
            elif isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.Call):
                return node.func.id
            else:
                print("WTF is this thing, build it in??", type(node))

        func = node.func
        func_name = visit_func(func)
        if isinstance(node, ast.Call):
            func_block = self.new_func_block()
            self.add_statement(func_block, node)
            func_block.name = func_name

            if self._callbuf:
                # Func block is argument of last block in self._callbuf
                self._callbuf[-1].args.append(func_block)
            else:
                # Not inside argument context.
                self.current_block.func_calls.append(func_name)
                self.current_block.func_blocks.append(func_block)

            self._callbuf.append(func_block)
            for arg in node.args:
                self.visit(arg)
            top = self._callbuf.pop()
            assert hash(top) == hash(func_block)
        else:
            self.current_block.func_calls.append(func_name)

    def visit_Assign(self, node: Assign) -> None:
        self.add_statement(self.current_block, node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: AnnAssign) -> None:
        self.add_statement(self.current_block, node)
        self.generic_visit(node)

    def visit_AugAssign(self, node: AugAssign) -> None:
        self.add_statement(self.current_block, node)
        self.generic_visit(node)

    def visit_Raise(self, node):
        # TODO
        pass

    def visit_Assert(self, node):
        self.add_statement(self.current_block, node)
        # New block for the case in which the assertion 'fails'.
        failblock = self.new_block()
        self.add_exit(self.current_block, failblock, invert(node.test))
        # If the assertion fails, the current flow ends, so the fail block is a
        # final block of the CFG.
        self.cfg.finalblocks.append(failblock)
        # If the assertion is True, continue the flow of the program.
        successblock = self.new_block()
        self.add_exit(self.current_block, successblock, node.test)
        self.current_block = successblock
        self.generic_visit(node)

    def visit_If(self, node: If) -> None:
        # If it already has something in it, we make a new block
        if self.current_block.statements:
            # Add the If statement at the beginning of the new block.
            cond_block = self.new_block()
            self.add_statement(cond_block, node)
            self.add_exit(self.current_block, cond_block)
            self.current_block = cond_block
        else:
            # Add the If statement at the end of the current block.
            self.add_statement(self.current_block, node)
        if any(isinstance(node.test, T) for T in (ast.Compare, ast.Call)):
            self.visit(node.test)
        # Create a new block for the body of the if. (storing the True case)
        if_block = self.new_block()

        self.add_exit(self.current_block, if_block, node.test)

        # Create a block for the code after the if-else.
        afterif_block = self.new_block()

        # New block for the body of the else if there is an else clause.
        if len(node.orelse) != 0:
            else_block = self.new_block()
            self.add_exit(self.current_block, else_block, invert(node.test))
            self.current_block = else_block
            # Visit the children in the body of the else to populate the block.
            for child in node.orelse:
                self.visit(child)
            self.add_exit(self.current_block, afterif_block)
        else:
            self.add_exit(self.current_block, afterif_block, invert(node.test))

        # Visit children to populate the if block.
        self.current_block = if_block
        for child in node.body:
            self.visit(child)
        self.add_exit(self.current_block, afterif_block)

        # Continue building the CFG in the after-if block.
        self.current_block = afterif_block

    def visit_While(self, node: While) -> None:
        loop_guard = self.new_loopguard()
        self.current_block = loop_guard
        self.add_statement(self.current_block, node)

        if isinstance(node.test, ast.Call):
            self.visit(node.test)
        # New block for the case where the test in the while is True.
        while_block = self.new_block()
        self.add_exit(self.current_block, while_block, node.test)

        # New block for the case where the test in the while is False.
        afterwhile_block = self.new_block()
        self.add_exit(self.current_block, afterwhile_block, invert(node.test))

        # Populate the while block.
        self.current_block = while_block
        for child in node.body:
            self.visit(child)
        self.add_exit(self.current_block, loop_guard)

        # Continue building the CFG in the after-while block.
        self.current_block = afterwhile_block

    def visit_For(self, node: For) -> None:
        loop_guard = self.new_loopguard()
        self.current_block = loop_guard
        self.add_statement(self.current_block, node)

        if isinstance(node.iter, ast.Call):
            self.visit(node.iter)
        # New block for the body of the for-loop.
        for_block = self.new_block()
        self.add_exit(self.current_block, for_block, node.iter)

        # Block of code after the for loop.
        afterfor_block = self.new_block()
        self.add_exit(self.current_block, afterfor_block)
        self.current_block = for_block

        # Populate the body of the for loop.
        for child in node.body:
            self.visit(child)
        self.add_exit(self.current_block, loop_guard)

        # Continue building the CFG in the after-for block.
        self.current_block = afterfor_block

    def visit_Break(self, node: Break) -> None:
        # TODO
        pass

    def visit_Continue(self, node):
        # TODO
        pass

    def visit_Import(self, node: Import) -> None:
        self.add_statement(self.current_block, node)

    def visit_ImportFrom(self, node: ImportFrom) -> None:
        self.add_statement(self.current_block, node)

    def visit_FunctionDef(self, node: FunctionDef) -> None:
        self.add_statement(self.current_block, node)
        self.new_functionCFG(node, asynchr=False)

    def visit_AsyncFunctionDef(self, node):
        self.add_statement(self.current_block, node)
        self.new_functionCFG(node, asynchr=True)

    def visit_Await(self, node):
        afterawait_block = self.new_block()
        self.add_exit(self.current_block, afterawait_block)
        self.generic_visit(node)
        self.current_block = afterawait_block

    def visit_Return(self, node: Return) -> None:
        self.add_statement(self.current_block, node)
        self.cfg.finalblocks.append(self.current_block)
        # Continue in a new block but without any jump to it -> all code after
        # the return statement will not be included in the CFG.
        self.current_block = self.new_block()

    def visit_Yield(self, node: Yield) -> None:
        self.cfg.asynchr = True
        afteryield_block = self.new_block()
        self.add_exit(self.current_block, afteryield_block)
        self.current_block = afteryield_block
