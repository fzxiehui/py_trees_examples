#!/usr/bin/env python3

import py_trees


# Foo 继承于 py_trees.behaviour.Behaviour
class Foo(py_trees.behaviour.Behaviour):

    def __init__(self, name):
        # 初始化父类,主要传入名字
        super().__init__(name=name)

        # 创建三个 黑板 
        self.blackboard = self.attach_blackboard_client(name="Foo Global")
        self.parameters = self.attach_blackboard_client(name="Foo Params", namespace="foo/parameters/")
        self.state = self.attach_blackboard_client(name="Foo State", namespace="foo/state/")

        # create a key 'foo_parameters_init' on the blackboard
        self.parameters.register_key("init", access=py_trees.common.Access.READ)
        # create a key 'foo_state_number_of_noodles' on the blackboard
        self.state.register_key("number_of_noodles", access=py_trees.common.Access.WRITE)

    # init 
    def initialise(self):
        self.state.number_of_noodles = self.parameters.init

    # 每次执行
    def update(self):
        self.state.number_of_noodles += 1
        self.feedback_message = self.state.number_of_noodles
        # 大于 5 成功
        if self.state.number_of_noodles > 5:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.RUNNING


# 创建 黑板
configuration = py_trees.blackboard.Client(name="App Config")
# 注册 foo/parameters/init
configuration.register_key("foo/parameters/init", access=py_trees.common.Access.WRITE)
# init 
configuration.foo.parameters.init = 3

foo = Foo(name="The Foo")
for i in range(1, 8):
    foo.tick_once()
    print("Number of Noodles: {}".format(foo.feedback_message))
