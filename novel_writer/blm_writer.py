# Stage 0 all parameters

# windows
root_dir = r'D:/CodeBase/Clara/chatbot/novel_writer'
train_data = r'train_data/shendiaoxialv.txt'
model_dir = r'/model'
# linux

train_data_ratio = 0.9
context_size = 10
batch_size = 32
try_load_existing_model = True
learning_rate = 1e-3
# val loss 5.2-5.3 18000 steps seems the limit
learning_iterations = 0
eval_interval = 50
eval_iters = 20
# Stage 0 end

# Stage 1 data prepration
# load data
from pathlib import Path
import logging
import random

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

data_file_path = Path(f'{root_dir}/{train_data}')
logger.info(f"Loading data from {data_file_path}.")
with open(data_file_path, 'r', encoding='gbk') as f:
    text = f.read()
logger.info(f"Loading data done.")
logger.info(f'number of total data text {len(text)}.')
charset = sorted(list(set(text)))
logger.info(f'number of total chars {len(charset)}.')
logger.info(f'first 100 charset {charset[0: 100]}.')
sample_text_size = 100
random_start = random.randint(0, len(text) - sample_text_size)
logger.info(f'random 100 text {text[random_start:random_start+sample_text_size]}.')

# encoder decoder
encoded_map = {char:i for i, char in enumerate(charset)}
decode_map = {i:char for i, char in enumerate(charset)}
encode = lambda input_text: [encoded_map[x] for x in input_text]
decode = lambda code: ''.join([decode_map[x] for x in code])

# encode text data
import torch
data = torch.tensor(encode(text), dtype=torch.long)
logger.info(f'data tensor size {data.shape}')
n = int(train_data_ratio * len(data))
train_data = data[:n]
val_data = data[n:]
logger.info(f'train data tensor size {train_data.shape}')
logger.info(f'val data tensor size {val_data.shape}')

# embedding
def get_batch(split:str):
    data = train_data if split == 'train' else val_data
    train_index = torch.randint(len(data) - context_size - 1, (batch_size,))
    x = torch.stack([data[i:i+context_size] for i in train_index])
    y = torch.stack([data[i+1:i+context_size+1] for i in train_index])
    return x, y


# Stage 1 end

# Stage 2 model setting
class BigramLanguageModel(torch.nn.Module):
    def __init__(self, charset_size):
        super().__init__()
        self.token_embedding_table = torch.nn.Embedding(charset_size, charset_size)

    def forward(self, idx, target=None):
        logits = self.token_embedding_table(idx)
        if target is None:
            return logits, None
        B, T, C = logits.shape
        logits = logits.view(B*T, C)
        target = target.view(B*T)
        loss = torch.nn.functional.cross_entropy(logits, target)
        return logits, loss
    
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, _loss = self(idx)
            logits = logits[:, -1, :]
            probs = torch.nn.functional.softmax(logits, dim=-1)
            new_char = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, new_char], dim=-1)
        return idx
    
model = BigramLanguageModel(len(charset))
model_file_name = f'm_{context_size}_{batch_size}.pt'
model_file_path_raw = f'{root_dir}/{model_dir}/{model_file_name}'
model_file_path = Path(model_file_path_raw)
if try_load_existing_model and model_file_path.exists():
    logger.info(f"Loading model from {model_file_path}.")
    model.load_state_dict(torch.load(model_file_path, weights_only=True))
    model.eval()
    logger.info(f"Loading model done.")

def generate_text(model, max_token_length):
    new_tokens = model.generate(torch.full((1,1), 0, dtype=torch.long), max_token_length)
    text = decode(new_tokens[0].tolist())
    logger.info(text)
logger.info(f"generated text at after model {'loaded' if try_load_existing_model else 'initialized'}")
generate_text(model, 100)

# Stage 2 end

# Stage 3 model training
def eval_loss(model, eval_iters):
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            context, target = get_batch(split)
            _logits, loss = model(context, target)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

model.train()
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
save_number = 0
for steps in range(learning_iterations):
    context, target = get_batch('train')
    logits, loss = model(context, target)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

    if steps % eval_interval == 0:
        loss = eval_loss(model, eval_iters)
        logger.info(f"step {steps} train loss {loss['train']:.4f} val loss {loss['val']:.4f}")
    if steps % 200 == 0:
        torch.save(model.state_dict(), Path(f'{model_file_path_raw}_{save_number % 2}'))
        save_number += 1


loss = eval_loss(model, eval_iters)
logger.info(f"after training {loss['train']:.4f} val loss {loss['val']:.4f}")
torch.save(model.state_dict(), model_file_path)
# Stage 3 end
# Stage 4 model generation
logger.info(f"generated text at after model trained")
generate_text(model, 100)
# Stage 4 end