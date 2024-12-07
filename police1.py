from manimlib import *
import numpy as np

class PoliceSearch(Scene):
    def construct(self):
        # Create three dots representing police officers with different colors
        officers = VGroup()
        viewfinders = VGroup()
        colors = [BLUE, RED, GREEN]
        
        for i, color in enumerate(colors):
            # Create dot (officer)
            officer = Dot(color=color)
            officer.move_to([-4 + 2*i, -2, 0])  # Start positions
            officers.add(officer)
            
            # Create viewfinder (line)
            viewfinder = Line(
                start=officer.get_center(),
                end=officer.get_center() + np.array([1, 1, 0]),
                color=color
            )
            viewfinders.add(viewfinder)
        
        # Add everything to scene
        self.play(
            *[Create(officer) for officer in officers],
            *[Create(viewfinder) for viewfinder in viewfinders]
        )
        
        # First movement: sweep across bottom
        self.play(
            *[
                officer.animate.move_to([-4 + 2*i, 0, 0])
                for i, officer in enumerate(officers)
            ],
            run_time=2
        )
        
        # Update viewfinders during movement
        def update_viewfinder(viewfinder, officer):
            viewfinder.put_start_and_end_on(
                officer.get_center(),
                officer.get_center() + np.array([1, 1, 0])
            )
        
        for i in range(3):
            viewfinders[i].add_updater(
                lambda v, o=officers[i]: update_viewfinder(v, o)
            )
        
        # Second movement: spread out to clear rooms
        self.play(
            officers[0].animate.move_to([-3, 2, 0]),
            officers[1].animate.move_to([0, 2, 0]),
            officers[2].animate.move_to([3, 2, 0]),
            run_time=2
        )
        
        # Rotate viewfinders
        self.play(
            *[
                Rotate(
                    viewfinders[i],
                    angle=TAU,
                    about_point=officers[i].get_center(),
                    rate_func=smooth
                ) for i in range(3)
            ],
            run_time=3
        )
        
        # Final sweep
        self.play(
            officers[0].animate.move_to([-3, -2, 0]),
            officers[1].animate.move_to([0, -2, 0]),
            officers[2].animate.move_to([3, -2, 0]),
            run_time=2
        )
        
        # Pause at the end
        self.wait()