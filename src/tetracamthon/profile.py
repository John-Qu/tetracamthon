from tetracamthon.stage import Spline, Stages


class YorkProfile(Spline):
    def __init__(self,
                 a_production,
                 whether_rebuild_stages=False,
                 ):
        self.stages = Stages(
            machine_production=a_production,
            whether_reload=False
        )
        self.stages.

