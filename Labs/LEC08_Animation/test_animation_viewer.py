import unittest

import animation_viewer as viewer


class AnimationViewerTests(unittest.TestCase):
    def test_configured_frames_fit_sprite_sheet(self):
        viewer.validate_clips(544, 416)

    def test_frame_source_y_uses_pico2d_bottom_origin(self):
        self.assertEqual(viewer.SpriteFrame(0, 0).bottom_origin(416), 368)

    def test_walk_cycle_has_sixteen_frames(self):
        self.assertEqual(len(viewer.WALK_CLIP.frames), 16)

    def test_starting_character_is_not_clipped_by_left_edge(self):
        half_width = viewer.FRAME_WIDTH * viewer.SPRITE_SCALE / 2
        self.assertGreaterEqual(viewer.START_X - half_width, 0)

    def test_move_toward_clamps_at_target(self):
        self.assertEqual(viewer.move_toward(790, 800, 20), 800)
        self.assertEqual(viewer.move_toward(10, 0, 20), 0)

    def test_jump_reaches_apex_and_transitions_to_attack(self):
        state = viewer.AnimationState(phase=viewer.Phase.JUMP)

        viewer.update_jump(state, viewer.JUMP_DURATION / 2)
        self.assertEqual(state.y, viewer.GROUND_Y + 180)

        viewer.update_jump(state, viewer.JUMP_DURATION / 2)
        self.assertEqual(state.y, viewer.GROUND_Y)
        self.assertIs(state.phase, viewer.Phase.ATTACK)

    def test_cycle_visits_actions_and_returns_to_left_start(self):
        state = viewer.AnimationState()
        visited = []

        for _ in range(210):
            previous_phase = state.phase
            viewer.update_state(state, 0.02)
            if state.phase is not previous_phase:
                visited.append(state.phase)

        self.assertEqual(
            visited[:4],
            [
                viewer.Phase.JUMP,
                viewer.Phase.ATTACK,
                viewer.Phase.WALK_TO_LEFT,
                viewer.Phase.WALK_TO_CENTER,
            ],
        )
        self.assertIn(viewer.Phase.WALK_TO_CENTER, visited)
        self.assertLessEqual(state.x, viewer.CENTER_X)


if __name__ == "__main__":
    unittest.main()
