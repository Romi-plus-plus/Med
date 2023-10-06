from typing import Any


class LabelDict:
    def __init__(self, labels: list[str], unk_label="[UNK]") -> None:
        self.unk_label = unk_label
        self.labels = [unk_label] + labels if unk_label not in labels else labels
        assert len(self.labels) == len(set(self.labels)), "ERROR: repeated labels appeared!"

    def __len__(self) -> int:
        return len(self.labels)

    def save_dict(self, save_path) -> None:
        with open(save_path, "w") as f:
            f.write("\n".join(self.labels))

    def encode(self, labels: str) -> int:
        if labels in self.labels:
            return self.labels.index(labels)
        else:
            return self.labels.index(self.unk_label)

    def decode(self, labels: int) -> str:
        return self.labels[labels]

    @classmethod
    def load_dict(cls, load_path: Any, **kwargs):
        with open(load_path, "r") as f:
            labels = f.read().strip("\n").split("\n")

        return cls(labels, **kwargs)
