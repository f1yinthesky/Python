# Stage 0 all parameters

# windows
root_dir = r'D:/CodeBase/Clara/chatbot/novel_writer'
train_data = r'train_data/shendiaoxialv.txt'
model_dir = r'/model'
# linux

train_data_ratio = 0.9
context_size = 100
batch_size = 32
num_embeddings = 16
try_load_existing_model = True
need_save_model = False
learning_rate = 1e-3
# bllm val loss 5.2
# 16 num embedding val loss 5.4-5.5
# single head llm val loss 5.3 with 8000  
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

charset_file_name = f'llm_{context_size}_{batch_size}.txt'
charset_file_path_raw = f'{root_dir}/{model_dir}/{charset_file_name}'
charset_file_path = Path(charset_file_path_raw)

def load_charset(charset_file_path):
    with open(charset_file_path, 'r', encoding='gbk') as f:
        charset = f.read()
    return list(charset)

def save_charset(charset, charset_file_path):
    with open(charset_file_path, 'w', encoding='gbk') as f:
        f.write(''.join(charset))

if try_load_existing_model and charset_file_path.exists():
    logger.info(f"Loading charset from {charset_file_path}.")
    charset = load_charset(charset_file_path)
    logger.info(f"Loading charset done.")
else:
    charset = sorted(list(set(text)))
if need_save_model:
    save_charset(charset, charset_file_path)

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
class Head(torch.nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.key = torch.nn.Linear(num_embeddings, head_size)
        self.query = torch.nn.Linear(num_embeddings, head_size)
        self.value = torch.nn.Linear(num_embeddings, head_size)
        self.register_buffer('tril', torch.tril(torch.ones(context_size, context_size)))

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)
        q = self.query(x)
        wei = k @ q.transpose(-2, -1) * C ** (-0.5)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        wei = torch.nn.functional.softmax(wei, dim=-1)
        v = self.value(x)
        out = wei @ v
        return out

class LargeLanguageModel(torch.nn.Module):
    def __init__(self, charset_size):
        super().__init__()
        self.token_embedding_table = torch.nn.Embedding(charset_size, num_embeddings)
        self.pos_embedding_table = torch.nn.Embedding(context_size, num_embeddings)
        self.sa_head = Head(num_embeddings)
        self.lm_head = torch.nn.Linear(num_embeddings, charset_size)


    def forward(self, idx, target=None):
        B, T = idx.shape
        token_embedding = self.token_embedding_table(idx) # B, T, num_embeddings
        pos_embedding = self.pos_embedding_table(torch.arange(T)) # T, num_embeddings
        x = token_embedding + pos_embedding # B, T, num_embeddings
        x = self.sa_head(x) # B, T, num_embeddings
        logits = self.lm_head(x) # B, T, charset_size
        if target is None:
            return logits, None
        B, T, C = logits.shape
        logits = logits.view(B*T, C)
        target = target.view(B*T)
        loss = torch.nn.functional.cross_entropy(logits, target)
        return logits, loss
    
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, _loss = self(idx[:, -context_size:])
            logits = logits[:, -1, :]
            probs = torch.nn.functional.softmax(logits, dim=-1)
            new_char = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, new_char], dim=-1)
        return idx
    
model = LargeLanguageModel(len(charset))
model_file_name = f'llm_{context_size}_{batch_size}.pt'
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

def save_model(model, model_file_path):
    if need_save_model:
        logger.info(f"Saving model to {model_file_path}.")
        torch.save(model.state_dict(), model_file_path)
        logger.info(f"Saving model done.")
        

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
        save_model(model, Path(f'{model_file_path_raw}_{save_number % 2}'))
        save_number += 1


loss = eval_loss(model, eval_iters)
logger.info(f"after training {loss['train']:.4f} val loss {loss['val']:.4f}")
save_model(model, model_file_path)
# Stage 3 end
# Stage 4 model generation
logger.info(f"generated text at after model trained")
generate_text(model, 1000)
# Stage 4 end