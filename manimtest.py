from manim import *


class MovingDotWithColorChange(Scene):
    def construct(self):
        # Define start and end points
        start_point = LEFT * 4
        end_point = RIGHT * 4

        # Create a dot at the start point
        dot = Dot(start_point, color=BLUE)
        dot.s = start_point
        dot.e = end_point
        self.add(dot)

        # Define an updater function for the dot
        def update_dot_colory(dot, dt):
            # Calculate the proportion of the dot's x position between start and end points
            proportion = np.linalg.norm(dot.get_center() - dot.s) / np.linalg.norm(
                dot.s - dot.e
            )
            # Interpolate the color based on the proportion

            if proportion <= 0.5:
                new_color = YELLOW

                dot = dot.set_color(new_color).animate(run_time=0)

        def update_dot_colorr(dot, dt):
            # Calculate the proportion of the dot's x position between start and end points
            proportion = np.linalg.norm(dot.get_center() - dot.s) / np.linalg.norm(
                dot.s - dot.e
            )
            # Interpolate the color based on the proportion

            if 0.9 >= proportion:
                new_color = RED

                dot.set_color(new_color)

        # Add the updater to the dot
        # dot.add_updater(update_dot_colory)
        dot.add_updater(update_dot_colorr)

        # Animate the dot moving to the end point
        self.play(dot.animate.move_to(end_point), run_time=4, rate_func=linear)

        # Remove the updater after the animation to prevent further updates
        dot.remove_updater(update_dot_colory)
        dot.remove_updater(update_dot_colorr)

        # Keep the final state for a moment before closing the scene
        self.wait(1)
