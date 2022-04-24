from collections import deque
import torch
import numpy as np
from utils import utilsTileTypes
from neural import *
from gameControls import *
import random, datetime

class PDAgent:
    tilesAntes = 0
    depthAntes = 0

    def __init__(self, save_dir, checkpoint=None):

        self.memory = deque(maxlen=100000)
        self.batch_size = 32
        self.exploration_rate = 1
        self.exploration_rate_decay = 0.99999975
        self.exploration_rate_min = 0.1
        self.gamma = 0.9

        self.burnin = 1e5 # min. experiences before training
        #self.burnin = 32  # min. experiences before training
        self.learn_every = 3  # no. of experiences between updates to Q_online
        self.sync_every = 1e4  # no. of experiences between Q_target & Q_online sync
        self.save_every = 2e4  # no. of experiences between saving PD Net
        self.save_dir = save_dir
        self.curr_step = 1
        self.action_dim = 11
        self.state_dim = 3072

        self.use_cuda = torch.cuda.is_available()
        #print(self.use_cuda)
        self.net = PDNet(self.state_dim, self.action_dim).float()

        if self.use_cuda:
            self.net = self.net.to(device='cuda')

        if checkpoint:
            self.load(checkpoint)

        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=0.00025)
        self.loss_fn = torch.nn.SmoothL1Loss()

    def act(self, state, tiles, fogOfWar, playerPos):  # possíveis ações

        action_list = [move_N,
                       move_S,
                       move_NO,
                       move_L,
                       move_NL,
                       move_SL,
                       move_SO,
                       move_O,
                       action_wait,
                       action_attack,
                       action_use,
                       ]
        #len(action_list) = 11

        if np.random.rand() < self.exploration_rate:  # explore
            #print(np.random.rand(), self.exploration_rate, "EXPLORE")
            action_idx = np.random.randint(self.action_dim)

        else:  # exploit
            state = torch.tensor(state)
            state = torch.FloatTensor(state).cuda() if self.use_cuda else torch.FloatTensor(state)
            state = state.unsqueeze(0)
            #print(np.random.rand(), self.exploration_rate, "EXPLOIT")
            action_values = self.net(state, model="online")
            action_idx = torch.argmax(action_values).item()

        #print(playerPos.reshape(32, 32))
        action_list[action_idx]()
        #print(action_idx, " - ", action_list[action_idx].__name__)
        penalize, movementLock, timetowait, playerPos, fogOfWar, gameReset = PDAgent.penalizeFunction(self, playerPos, action_idx, tiles, fogOfWar)
        #print(playerPos.reshape(32, 32))

        self.exploration_rate *= self.exploration_rate_decay
        self.exploration_rate = max(self.exploration_rate_min, self.exploration_rate)

        self.curr_step += 1  # incrementar step


        #time.sleep(timetowait)
        #if movementLock: action_ESC()
        return action_idx, penalize, playerPos, gameReset

    def calcReward(self, penalize, tiles, fogOfWar, gameReset, playerPos):

        # tiles = read_tiles()
        # fogOfWar = read_fog_of_war()
        #playerPos = read_playerPos()
        tiles_visitados = 0
        # print(action)

        reward = 0
        pos = 1
        # penalize = 0

        for pos in range(1023):
            if fogOfWar[pos] == 0 and tiles[pos] != 4 or fogOfWar[pos] == 1 and tiles[
                pos] != 4:  # tiles "caminháveis" que ainda não estão mapeados
                # 0xff000000 4278190080 #invisible # 2
                # 0xcc111111 3423670545 # visited # 1
                # 0x0 0 # visible # 0
                tiles_visitados = tiles_visitados + 1

            if playerPos[pos] == 1 and tiles[
                pos] == 29:  # se o personagem pisa numa placa, aparece uma mensagem que tranca o jogo
                penalize = penalize + 100  # penaliza essa ação
                #action_ESC()  # aperta ESC pra fechar a mensagem

            if playerPos[pos] == 1 and tiles[
                pos] == 7:  # se o personagem pisa numa escada pra cima
                penalize = penalize + 100  # penaliza essa ação
                #action_ESC()  # aperta ESC pra fechar a mensagem

        # print(playerPos[pos], tiles[pos])

        tiles_free = np.count_nonzero(np.array(tiles) != 4)  # número de tiles que não é parede

        #if read_depth() > 1:
        #    rewardDepth = (read_depth() - PDAgent.depthAntes) * 999 * 3  # se descer um nível, dá um reward grande
        #else:
        #    rewardDepth = 0

        rewardExploration = (tiles_visitados - PDAgent.tilesAntes) * 100  # a cada step, os novos tiles descobertos viram reward

        if PDAgent.tilesAntes == 0:
            PDAgent.depthAntes = 1
            PDAgent.tilesAntes = tiles_visitados
            rewardExploration = 0
            tiles_free = 0
            #tiles_visitados = 0
            #return rewardExploration  # , tiles_free, tiles_visitados

        #if rewardDepth != 0:  # quando sobe ou desce o nivel, os valores precisam carregar, isso faz com que espere um pouco e zere os valores pra não calcular reward indevido
        #    time.sleep(3)
            #PDAgent.depthAntes = 0  # se um mapa tem nº de tiles diferente do próximo, ele calculava reward incorreto
        #    PDAgent.tilesAntes = 0
        #    rewardExploration = 0
            tiles_free = 0
        #    tiles_visitados = 0
            #return rewardDepth



        PDAgent.depthAntes = 1 #read_depth()
        PDAgent.tilesAntes = tiles_visitados  # antes da próxima iteração

        # print(read_depth(), tiles_free, tiles_visitados, PDAgent.tilesAntes, rewardExploration, rewardDepth)  # reward exploração nivel

        totalReward = rewardExploration + 0 - penalize
        #totalReward = rewardExploration + rewardDepth - penalize
        # print(action, " - ", self.act.action_list[action].__name__)

        # time.sleep(2)
        gameReset = False

        if gameReset:
            PDAgent.depthAntes = 0
            PDAgent.tilesAntes = 0
            penalize = 0
            tiles_visitados = 0
            totalReward = 0
            gameReset = False

        print("step: ", self.curr_step, "reward: ", totalReward)
        return totalReward
        # return rewardExploration, tiles_free, tiles_visitados, rewardDepth

    def step(self, tiles, fogOfWar, playerPos):

        #tiles = read_tiles()
        #fogOfWar = read_fog_of_war()
        #playerPos = read_playerPos()

        tilesTensor = torch.tensor(tiles)
        fogOfWarTensor = torch.tensor(fogOfWar)
        playerPosTensor = torch.tensor(playerPos)

        next_state = torch.stack([tilesTensor, fogOfWarTensor, playerPosTensor])
        next_state = next_state.reshape(3, 32, 32)

        return next_state

    def cache(self, state, next_state, action, reward):
        """
        Store the experience to self.memory (replay buffer)
        Inputs:
        state (LazyFrame),
        next_state (LazyFrame),
        action (int),
        reward (float),
        done(bool))
        """

        state = torch.tensor(state).cuda() if self.use_cuda else torch.tensor(state)
        state = state.reshape(3, 32, 32)
        next_state = torch.tensor(next_state).cuda() if self.use_cuda else torch.tensor(next_state)
        next_state = next_state.reshape(3, 32, 32)
        action = torch.tensor([action]).cuda() if self.use_cuda else torch.tensor([action])
        reward = torch.tensor([reward]).cuda() if self.use_cuda else torch.tensor([reward])


        self.memory.append((state, next_state, action, reward))

    def recall(self):
        """
        Retrieve a batch of experiences from memory
        """
        batch = random.sample(self.memory, self.batch_size)
        # print(batch)
        state, next_state, action, reward = map(torch.stack, zip(*batch))
        return state, next_state, action.squeeze(), reward.squeeze()

    def td_estimate(self, state, action):
        current_Q = self.net(state, model='online')[np.arange(0, self.batch_size), action]  # Q_online(s,a)
        return current_Q

    @torch.no_grad()
    def td_target(self, reward, next_state):
        next_state_Q = self.net(next_state, model='online')
        best_action = torch.argmax(next_state_Q, axis=1)
        next_Q = self.net(next_state, model='target')[np.arange(0, self.batch_size), best_action]
        # return next_Q
        return (reward * self.gamma * next_Q).float()

    def update_Q_online(self, td_estimate, td_target):
        loss = self.loss_fn(td_estimate, td_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def sync_Q_target(self):
        self.net.target.load_state_dict(self.net.online.state_dict())

    def learn(self):

        if self.curr_step % self.sync_every == 0:
            self.sync_Q_target()
            #print("Syncing model...")

        if self.curr_step % self.save_every == 0:
            self.save()
            #print("Saving model...")

        if self.curr_step < self.burnin:
            return None, None

        if self.curr_step % self.learn_every != 0:  # explore?
            return None, None

        # Sample from memory
        state, next_state, action, reward = self.recall()

        # state = state.unsqueeze(0)
        # Get TD Estimate
        td_est = self.td_estimate(state, action)

        # next_state = next_state.unsqueeze(0)
        # Get TD Target
        td_tgt = self.td_target(reward, next_state)

        # Backpropagate loss through Q_online
        loss = self.update_Q_online(td_est, td_tgt)

        return (td_est.mean().item(), loss)

    def save(self):
        save_path = self.save_dir / f"PD_net_{int(self.curr_step)}.chkpt"
        torch.save(
            dict(
                model=self.net.state_dict(),
                exploration_rate=self.exploration_rate
            ),
            save_path
        )
        print(f"PDNet saved to {save_path} at step {self.curr_step}")

    def load(self, load_path):
        if not load_path.exists():
            raise ValueError(f"{load_path} não existe")

        ckp = torch.load(load_path, map_location=('cuda' if self.use_cuda else 'cpu'))
        exploration_rate = ckp.get('exploration_rate')
        state_dict = ckp.get('model')

        print(f"Loading model at {load_path} with exploration rate {exploration_rate}")
        self.net.load_state_dict(state_dict)
        self.exploration_rate = exploration_rate

    def penalizeFunction(self, playerPos, action_idx, tiles, fogOfWar):

        # print(playerPos, action_idx, tiles)

        movementLock = False
        penalize = 0
        timetowait = 0
        monsterCount = 0
        depthLevel = 1
        gameReset = False
        goodTiles, badTiles, worstTiles, lockTiles, goalTiles = utilsTileTypes()

        for pos in range(0, 1023):
            # SE ANDAR EM DIREÇÃO A TILE DE PAREDE
            if playerPos[pos] == 1 and action_idx == 0 and tiles[pos - 32] in badTiles:
                penalize = 50  # N
                break
            if playerPos[pos] == 1 and action_idx == 1 and tiles[pos + 32] in badTiles:
                penalize = 50  # S
                break
            if playerPos[pos] == 1 and action_idx == 2 and tiles[pos - 33] in badTiles:
                penalize = 50  # NO
                break
            if playerPos[pos] == 1 and action_idx == 3 and tiles[pos + 1] in badTiles:
                penalize = 50  # L
                break
            if playerPos[pos] == 1 and action_idx == 4 and tiles[pos - 31] in badTiles:
                penalize = 50  # NL
                break
            if playerPos[pos] == 1 and action_idx == 5 and tiles[pos + 33] in badTiles:
                penalize = 50  # SL
                break
            if playerPos[pos] == 1 and action_idx == 6 and tiles[pos + 31] in badTiles:
                penalize = 50  # SO
                break
            if playerPos[pos] == 1 and action_idx == 7 and tiles[pos - 1] in badTiles:
                penalize = 50  # O
                break

            # SE ANDAR EM DIREÇÃO A UM CHASM (TRANCA O JOGO COM UMA MENSAGEM)
            if playerPos[pos] == 1 and action_idx == 0 and tiles[pos - 32] in lockTiles:
                penalize = 100
                movementLock = True
                break
            if playerPos[pos] == 1 and action_idx == 1 and tiles[pos + 32] in lockTiles:
                penalize = 100
                movementLock = True
                break
            if playerPos[pos] == 1 and action_idx == 2 and tiles[pos - 33] in lockTiles:
                penalize = 100
                movementLock = True
                break
            if playerPos[pos] == 1 and action_idx == 3 and tiles[pos + 1] in lockTiles:
                penalize = 100
                movementLock = True
                break
            if playerPos[pos] == 1 and action_idx == 4 and tiles[pos - 31] in lockTiles:
                penalize = 100
                movementLock = True
                break
            if playerPos[pos] == 1 and action_idx == 5 and tiles[pos + 33] in lockTiles:
                penalize = 100
                movementLock = True
                break
            if playerPos[pos] == 1 and action_idx == 6 and tiles[pos + 31] in lockTiles:
                penalize = 100
                movementLock = True
                break
            if playerPos[pos] == 1 and action_idx == 7 and tiles[pos - 1] in lockTiles:
                penalize = 100
                movementLock = True
                break

            if playerPos[pos] == 1 and action_idx == 10 and tiles[pos] == 8:
                #if playerPos[pos] == 1 and action_idx == 10 and tiles[pos] == 8:
                penalize = -5000 * np.count_nonzero(np.array(fogOfWar) == 1) # se o player dar use em tile que é escada pra baixo = reward * quantos tiles foram descobertos
                gameReset = True
                break
            if playerPos[pos] == 1 and action_idx == 10 and tiles[pos] != 8:
                penalize = 100  # se o player dar action_use em algum tile que não seja escada pra baixo
                break
            if playerPos[pos] == 1 and action_idx == 10 and tiles[pos] == 7 and depthLevel == 1:
                penalize = 1000  # se o player dar action_use no tile de escada pra cima no nivel 1
                movementLock = True
                break
            if playerPos[pos] == 1 and action_idx == 10 and tiles[pos] == 7:
                penalize = 2500  # se o player dar action_use em uma escada > sobe um nível (ruim)
                break
                #timetowait = 5

            # SE ANDAR EM LOCAL ABERTO = bom
            if playerPos[pos] == 1 and action_idx == 0 and tiles[pos - 32] in goodTiles:
                penalize = -10  # N
                playerPos[pos] = 0
                playerPos[pos - 32] = 1
                fogOfWar[pos] = 1
                break

            if playerPos[pos] == 1 and action_idx == 1 and tiles[pos + 32] in goodTiles:
                penalize = -10  # S
                playerPos[pos] = 0
                playerPos[pos + 32] = 1
                fogOfWar[pos] = 1
                break

            if playerPos[pos] == 1 and action_idx == 2 and tiles[pos - 33] in goodTiles:
                penalize = -10  # NO
                playerPos[pos] = 0
                playerPos[pos - 33] = 1
                fogOfWar[pos] = 1
                break

            if playerPos[pos] == 1 and action_idx == 3 and tiles[pos + 1] in goodTiles:
                penalize = -10  # L
                playerPos[pos] = 0
                playerPos[pos + 1] = 1
                fogOfWar[pos] = 1
                break

            if playerPos[pos] == 1 and action_idx == 4 and tiles[pos - 31] in goodTiles:
                penalize = -10  # NL
                playerPos[pos] = 0
                playerPos[pos - 31] = 1
                fogOfWar[pos] = 1
                break

            if playerPos[pos] == 1 and action_idx == 5 and tiles[pos + 33] in goodTiles:
                penalize = -10  # SL
                playerPos[pos] = 0
                playerPos[pos + 33] = 1
                fogOfWar[pos] = 1
                break

            if playerPos[pos] == 1 and action_idx == 6 and tiles[pos + 31] in goodTiles:
                penalize = -10  # SO
                playerPos[pos] = 0
                playerPos[pos + 31] = 1
                fogOfWar[pos] = 1
                break

            if playerPos[pos] == 1 and action_idx == 7 and tiles[pos - 1] in goodTiles:
                penalize = -10  # O
                playerPos[pos] = 0
                playerPos[pos - 1] = 1
                fogOfWar[pos] = 1
                break

            # SE ATACAR UM MONSTRO EM RODA
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos - 32] == 2:
                penalize = -500  # N
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos + 32] == 2:
                penalize = -500  # S
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos - 33] == 2:
                penalize = -500  # NO
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos + 1] == 2:
                penalize = -500  # L
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos - 31] == 2:
                penalize = -500  # NL
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos + 33] == 2:
                penalize = -500  # SL
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos + 31] == 2:
                penalize = -500  # SO
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos - 1] == 2:
                penalize = -500  # O
                break

            # SE ATACAR QUANDO NAO TEM MONSTRO
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos - 32] == 0:
                penalize = 100  # N
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos + 32] == 0:
                penalize = 100  # S
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos - 33] == 0:
                penalize = 100  # NO
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos + 1] == 0:
                penalize = 100  # L
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos - 31] == 0:
                penalize = 100  # NL
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos + 33] == 0:
                penalize = 100  # SL
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos + 31] == 0:
                penalize = -100  # SO
                break
            if playerPos[pos] == 1 and action_idx == 9 and playerPos[pos - 1] == 0:
                penalize = 100  # O
                break

            # SE TIVER MAIS DE UM MONSTRO EM VOLTA, PRA REDE APRENDER A LUTAR COM UM POR VEZ
            if playerPos[pos] == 1 and playerPos[pos - 32] == 2:
                monsterCount = monsterCount + 1
            if playerPos[pos] == 1 and playerPos[pos + 32] == 2:
                monsterCount = monsterCount + 1
            if playerPos[pos] == 1 and playerPos[pos - 33] == 2:
                monsterCount = monsterCount + 1
            if playerPos[pos] == 1 and playerPos[pos + 1] == 2:
                monsterCount = monsterCount + 1
            if playerPos[pos] == 1 and playerPos[pos - 31] == 2:
                monsterCount = monsterCount + 1
            if playerPos[pos] == 1 and playerPos[pos + 33] == 2:
                monsterCount = monsterCount + 1
            if playerPos[pos] == 1 and playerPos[pos + 31] == 2:
                monsterCount = monsterCount + 1
            if playerPos[pos] == 1 and playerPos[pos - 1] == 2:
                monsterCount = monsterCount + 1

            if action_idx == 8:
                penalize = 50  # WAIT?

        if monsterCount > 1:
            penalize = penalize + monsterCount * 350
            timetowait = 0 * monsterCount

        return penalize, movementLock, timetowait, playerPos, fogOfWar, gameReset
