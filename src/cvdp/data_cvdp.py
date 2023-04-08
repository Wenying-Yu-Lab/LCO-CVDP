from cvdp.base import *


def to_csv(data: List[Dict[any,any]], file_path: str) -> None:
    fn = refine_path(file_path)
    with open(fn, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

def from_csv(file_path: str) -> List[Dict]:
    fn = refine_path(file_path)
    with open(fn, 'r', encoding=auto_enco(fn)) as f:
        data = list(csv.DictReader(f))
    return data
