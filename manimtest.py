from manim import *

class SequentialDotAnimation(Scene):
    def construct(self):
        d1 = Dot(LEFT,color=RED).scale(0.5)
        d2 = Dot(RIGHT,color=RED).scale(0.5)
        self.add(d1)
        animatio = ReplacementTransform(d1,d2,run_time=3,rate_functions=linear)
        
        self.play(animatio)


        
        
