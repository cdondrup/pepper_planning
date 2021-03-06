#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
from pnp_plugin_server.pnp_simple_plugin_server import PNPSimplePluginServer
from pepper_engage_human.msg import EngageHumanAction, EngageHumanResult
from pnp_msgs.msg import ActionResult


class EngageHuman(object):
    def __init__(self, name):
        rospy.loginfo("Starting %s ..." % name)
        self._ps = PNPSimplePluginServer(
            name=name,
            ActionSpec=EngageHumanAction,
            execute_cb=self.execute_cb,
            auto_start=False
        )
        self._ps.start()
        rospy.loginfo("... done")

    def execute_cb(self, goal):
        rospy.loginfo("Engaging human '%s'" % (goal.id,))
        res = EngageHumanResult()
#        Has to be done in the end of the dialogue so the controller is blocked till it is over.
        res.result.append(ActionResult(cond="engaged__"+goal.interactant_id+"__"+goal.text, truth_value=True))
        if self._ps.is_preempt_requested():
            self._ps.set_preempted()
        else:
            self._ps.set_succeeded(res)

if __name__ == "__main__":
    rospy.init_node("engage_human")
    EngageHuman(rospy.get_name())
    rospy.spin()

