from flask import current_app, g
from app.api_driver import get_api_driver
import tensorflow as tf
from ampligraph.latent_features.models.EmbeddingModel import (
    register_model,
    EmbeddingModel,
)
import time


@register_model("NormE")
class NormE(EmbeddingModel):
    def _fn(self, e_s, e_p, e_o):
        import tensorflow as tf

        return tf.negative(
            tf.math.abs(
                tf.norm(
                    e_s - e_o,
                    ord=self.embedding_model_params.get("norm", 1),
                    axis=1,
                )
                - tf.norm(e_p)
            )
        )

    def _initialize_parameters(self):
        timestamp = int(time.time() * 1e6)
        tensor = tf.stack([tf.one_hot(0, self.internal_k), tf.zeros(self.internal_k)])
        if not self.dealing_with_large_graphs:
            self.ent_emb = tf.get_variable(
                "ent_emb_{}".format(timestamp),
                shape=[len(self.ent_to_idx), self.internal_k],
                initializer=self.initializer.get_entity_initializer(
                    len(self.ent_to_idx), self.internal_k
                ),
                dtype=tf.float32,
            )
            self.rel_emb = tf.get_variable(
                "rel_emb_{}".format(timestamp),
                trainable=False,
                initializer=tensor,
                dtype=tf.float32,
            )
        else:
            # initialize entity embeddings to zero (these are reinitialized every batch by batch embeddings)
            self.ent_emb = tf.get_variable(
                "ent_emb_{}".format(timestamp),
                shape=[self.batch_size * 2, self.internal_k],
                initializer=tf.zeros_initializer(),
                dtype=tf.float32,
            )
            self.rel_emb = tf.get_variable(
                "rel_emb_{}".format(timestamp),
                trainable=False,
                initializer=tensor,
                dtype=tf.float32,
            )
        print(self.rel_to_idx)


def embedComprehensive():
    triples = get_api_driver().triple.get_aggregated_triple()
    import numpy as np

    trainig_set = np.array(
        [(triple["h_name"], triple["r_name"], triple["t_name"]) for triple in triples]
    )
    from ampligraph.latent_features import TransE

    model = NormE(
        batches_count=50,
        epochs=50000,
        k=3,
        eta=0,
        optimizer="adam",
        optimizer_params={"lr": 1e-4},
        loss="multiclass_nll",
        regularizer="LP",
        regularizer_params={"p": 3, "lambda": 1e-5},
        seed=0,
        verbose=True,
        embedding_model_params={"negative_corruption_entities": []},
    )
    model.fit(
        trainig_set,
        early_stopping=True,
        early_stopping_params={"x_valid": trainig_set, "corruption_entities": []},
    )
    print(model.trained_model_params[1][model.rel_to_idx["Prerequisite of"]])
    print(model.trained_model_params[1][model.rel_to_idx["Subtopic in"]])
    for ent in model.ent_to_idx:
        print(ent)
        print(model.trained_model_params[0][model.ent_to_idx[ent]])
