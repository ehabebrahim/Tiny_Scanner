class Node:
    def __init__(self, token, code, shape):
        self.token_value = token
        self.code_value = code
        self.shape = shape
        self.children = []
        self.sibling = None
        self.index = None

    def set_children(self, child):
        try:
            assert isinstance(child, list)
            for i in child:
                self.children.append(i)
        except:
            self.children.append(child)

    def set_sibling(self, child):
        self.sibling = child


class parser:
    nodes_table = {}
    tmp_index = 0
    edges_table = []

    def __init__(self):
        self.token = str
        self.tokens_list = ['identifier', ':=',
                            'identifier', '+', 'number']
        self.code_list = ['x', ':=', 'x', '+', '5']
        self.tmp_index = 0
        self.token = self.tokens_list[self.tmp_index]
        self.parse_tree = None
        self.nodes_table = None
        self.edges_table = None
        self.same_rank_nodes = []

    def set_tokens_list_and_code_list(self, token, code):
        self.code_list = code
        self.tokens_list = token
        self.tmp_index = 0
        self.token = self.tokens_list[self.tmp_index]

    def next_token(self):
        if(self.tmp_index == len(self.tokens_list)-1):
            return False  # welcome to the end of the list
        self.tmp_index = self.tmp_index + 1
        self.token = self.tokens_list[self.tmp_index]
        return True

    def match(self, x):
        if self.token == x:
            self.next_token()
            return True
        else:
            raise ValueError('Token Mismatch', self.token)

    def statement(self):
        if self.token == 'if':
            child = self.if_stmt()
            return child
        elif self.token == 'repeat':
            child = self.repeat_stmt()
            return child
        elif self.token == 'identifier':
            child = self.assign_stmt()
            return child
        elif self.token == 'read':
            child = self.read_stmt()
            return child
        elif self.token == 'write':
            child = self.write_stmt()
            return child
        else:
            raise ValueError('SyntaxError', self.token)

    def stmt_sequence(self):
        child = self.statement()
        p = child
        while self.token == ';':
            q = Node(None, None, None)
            self.match(';')
            q = self.statement()
            if q == None:
                break
            else:
                if child == None:
                    child = p = q
                else:
                    p.set_sibling(q)
                    p = q
        return child

    def factor(self):
        if self.token == '(':
            self.match('(')
            child = self.exp()
            self.match(')')
        elif self.token == 'number':
            child = Node(
                'CONSTANT', '(' + self.code_list[self.tmp_index] + ')', 'o')
            self.match('number')
        elif self.token == 'identifier':
            child = Node('IDENTIFIER',
                     '(' + self.code_list[self.tmp_index] + ')', 'o')
            self.match('identifier')
        else:
            raise ValueError('SyntaxError', self.token)
            return False
        return child

    def term(self):
        child = self.factor()
        while self.token == '*' or self.token == '/':
            node = Node(
                'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
            node.set_children(child)
            child = node
            self.mulop()
            node.set_children(self.factor())
        return child

    def simple_exp(self):
        child = self.term()
        while self.token == '+' or self.token == '-':
            node = Node(
                'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
            node.set_children(child)
            child = node
            self.addop()
            child.set_children(self.term())
        return child

    def exp(self):
        child = self.simple_exp()
        if self.token == '<' or self.token == '=' or self.token == '>':
            node = Node(
                'OPERATOR', '(' + self.code_list[self.tmp_index] + ')', 'o')
            node.set_children(child)
            child = node
            self.comparison_op()
            child.set_children(self.simple_exp())
        return child

    def if_stmt(self):
        node = Node('IF', '', 's')
        if self.token == 'if':
            self.match('if')
            node.set_children(self.exp())
            self.match('then')
            node.set_children(self.stmt_sequence())
            if self.token == 'else':
                self.match('else')
                node.set_children(self.stmt_sequence())
            self.match('end')
        return node

    def comparison_op(self):
        if self.token == '<':
            self.match('<')
        elif self.token == '=':
            self.match('=')
        elif self.token == '>':
            self.match('>')

    def addop(self):
        if self.token == '+':
            self.match('+')
        elif self.token == '-':
            self.match('-')

    def mulop(self):
        if self.token == '*':
            self.match('*')
        elif self.token == '/':
            self.match('/')

    def repeat_stmt(self):
        node = Node('REPEAT', '', 's')
        if self.token == 'repeat':
            self.match('repeat')
            node.set_children(self.stmt_sequence())
            self.match('until')
            node.set_children(self.exp())
        return node

    def assign_stmt(self):
        node = Node('ASSIGN', '(' + self.code_list[self.tmp_index] + ')', 's')
        self.match('identifier')
        self.match(':=')
        node.set_children(self.exp())
        return node

    def read_stmt(self):
        node = Node('READ', '(' + self.code_list[self.tmp_index+1] + ')', 's')
        self.match('read')
        self.match('identifier')
        return node

    def write_stmt(self):
        node = Node('WRITE', '', 's')
        self.match('write')
        node.set_children(self.exp())
        return node

    def create_nodes_table(self, args=None):
        if args == None:
            self.parse_tree.index = parser.tmp_index
            parser.nodes_table.update(
                {parser.tmp_index: [self.parse_tree.token_value, self.parse_tree.code_value, self.parse_tree.shape]})
            parser.tmp_index = parser.tmp_index+1
            if len(self.parse_tree.children) != 0:
                for i in self.parse_tree.children:
                    self.create_nodes_table(i)
            if self.parse_tree.sibling != None:
                self.create_nodes_table(self.parse_tree.sibling)
        else:
            args.index = parser.tmp_index
            parser.nodes_table.update(
                {parser.tmp_index: [args.token_value, args.code_value, args.shape]})
            parser.tmp_index = parser.tmp_index+1
            if len(args.children) != 0:
                for i in args.children:
                    self.create_nodes_table(i)
            if args.sibling != None:
                self.create_nodes_table(args.sibling)

    def create_edges_table(self, args=None):
        if args == None:
            if len(self.parse_tree.children) != 0:
                for i in self.parse_tree.children:
                    parser.edges_table.append((self.parse_tree.index, i.index))
                for j in self.parse_tree.children:
                    self.create_edges_table(j)
            if self.parse_tree.sibling != None:
                parser.edges_table.append(
                    (self.parse_tree.index, self.parse_tree.sibling.index))
                self.same_rank_nodes.append(
                    [self.parse_tree.index, self.parse_tree.sibling.index])
                self.create_edges_table(self.parse_tree.sibling)
        else:
            if len(args.children) != 0:
                for i in args.children:
                    parser.edges_table.append((args.index, i.index))
                for j in args.children:
                    self.create_edges_table(j)
            if args.sibling != None:
                parser.edges_table.append((args.index, args.sibling.index))
                self.same_rank_nodes.append([args.index, args.sibling.index])
                self.create_edges_table(args.sibling)

    def run(self):
        self.parse_tree = self.stmt_sequence()  # create parse tree
        self.create_nodes_table()  # create nodes_table
        self.create_edges_table()  # create edges_table
        self.edges_table = parser.edges_table  # save edges_table
        self.nodes_table = parser.nodes_table  # save nodes_table
        if self.tmp_index == len(self.tokens_list)-1:
            print('success')
        elif self.tmp_index < len(self.tokens_list):
            raise ValueError('SyntaxError', self.token)

    def clear_tables(self):
        self.nodes_table.clear()
        self.edges_table.clear()