import json
import os

from ..core.constants import SAVE_DIR

class Save_manager:
    def convert_score_to_json(self, score):
        data = {"score": score}
        return data


    def save_score(self, score):
        score.save_best_score()
        score_data = self.convert_score_to_json(score.best_score)

        with open(SAVE_DIR, 'w+') as f:
            json.dump(score_data, f, )


    def load_score(self):
        if os.path.exists(SAVE_DIR):
            with open(SAVE_DIR, 'r') as f:
                data = json.load(f)
            
            return data["score"]
        return 0



            
        
