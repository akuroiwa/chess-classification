from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
import torch
import os

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

class ChessClassification(object):

    def __init__(self, output_dir='chess-outputs/'):

        # Optional model configuration
        self.model_args = ClassificationArgs(num_train_epochs=1)
        # self.model_args.reprocess_input_data = True
        self.model_args.output_dir = output_dir
        self.model_args.overwrite_output_dir = True
        # self.model_args.use_cached_eval_features = True
        # self.model_args.silent = True
        # self.model_args.logging_steps = 0

        self.cuda_available = torch.cuda.is_available()

        # Create a ClassificationModel
        if os.path.exists(os.path.join(output_dir, "pytorch_model.bin")):
            self.model = ClassificationModel(
                # 'bert',
                'electra',
                # "roberta",
                output_dir,
                num_labels=3,
                args=self.model_args,
                use_cuda=self.cuda_available
                )
        else:
            self.model = ClassificationModel(
                # 'bert',
                # 'bert-base-cased',
                'electra',
                'google/electra-small-discriminator',
                # 'google/electra-base-discriminator',
                # "roberta",
                # "roberta-base",
                num_labels=3,
                args=self.model_args,
                use_cuda=self.cuda_available
                )

    def train_and_eval(self, train_json, eval_json):
        train_df = pd.read_json(train_json)
        # Train the model
        self.model.train_model(train_df)

        eval_df = pd.read_json(eval_json)
        # Evaluate the model
        # result, model_outputs, wrong_predictions = self.model.eval_model(eval_df)
        result, model_outputs, wrong_predictions = self.model.eval_model(eval_df, verbose=False, silent=True)

    def predict_fen(self, fen):
        # Make predictions with the model
        fen_token = fen.replace("/", " ")
        # fen_token = ' '.join(list(fen))
        prediction, raw_outputs = self.model.predict([fen_token])
        # print(prediction, raw_outputs)
        return prediction, raw_outputs
