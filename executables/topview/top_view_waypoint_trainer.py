from training_utils.visual_navigation_trainer import VisualNavigationTrainer
from models.visual_navigation.top_view.top_view_waypoint_model import TopViewWaypointModel
import os


class TopViewWaypointTrainer(VisualNavigationTrainer):
    """
    Create a trainer that regress on the optimal waypoint using the top-view occupancy maps.
    """
    simulator_name = 'Topview_NN_Waypoint_Simulator'

    def create_model(self, params=None):
        self.model = TopViewWaypointModel(self.p)

    def _modify_planner_params(self, p):
        """
        Modifies a DotMap parameter object
        with parameters for a NNWaypointPlanner
        """
        from planners.nn_waypoint_planner import NNWaypointPlanner

        p.planner_params.planner = NNWaypointPlanner
        p.planner_params.model = self.model

    def _summary_dir(self):
        """
        Returns the directory name for tensorboard
        summaries
        """
        return os.path.join(self.p.session_dir, 'summaries', 'nn_waypoint')


if __name__ == '__main__':
    TopViewWaypointTrainer().run()