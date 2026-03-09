from pacman.systems.save_manager import Save_manager
from pacman.systems.score import Score

class TestSaveScore:

    def test_save_and_load(self):
        score = Score()
        score.best_score = 50

        save_manager = Save_manager()
        save_manager.save_score(score)

        loaded_score = save_manager.load_score()
        assert loaded_score == score.get_current_best_score()
    
    def test_score_get(self): 
        score = Score()
        assert score.get_current_score() == 0

    def test_score_add(self):
        score = Score()
        score_val = 50

        score.add(score_val)
        assert score.get_current_score() == score_val 

    def test_score_get_best(self):
        score = Score()
        score_val = 100
        best_score_val = 150

        score.add(score_val)
        score.best_score = best_score_val

        assert score.get_current_best_score() == best_score_val

    def test_score_best_Save(self):
        score = Score()
        new_best_score = 150

        score.best_score = 100
        score.add(new_best_score)

        score.save_best_score()
        assert score.best_score == new_best_score

        


