
from math import *
from random import *
import pickle
import pygame
import inspect

__author__ = 'Max Chiang'

from ChiangObjectives import *

import time

import sys
path = sys.path[0]
if not path: path = sys.path[1]

def STAB(PokeType,PokeType2,AttType):
                if PokeType==AttType or PokeType2==AttType:
                                return 1.5
                else:
                                return 1

def BonusCalc(typ,oppType,oppType2):
                bonus=1
                for i in range(0,len(eval(typ+"Bonus")[typ])):
                                if oppType==(eval(typ+"Bonus"))[typ][i][0]:
                                                print(oppType)
                                                print((eval(typ+"Bonus"))[typ][i][1],"a")
                                                bonus*=(eval(typ+"Bonus"))[typ][i][1]
                                                print(bonus)

                for i in range(0,len(eval(typ+"Bonus")[typ])):
                                if oppType2!=oppType:
                                                if oppType2==(eval(typ+"Bonus"))[typ][i][0]:
                                                                bonus*=(eval(typ+"Bonus"))[typ][i][1]
                                                                print(bonus)

                effect = "was fine. "
                if bonus==0:
                                effect="had no effect."
                if bonus==1/2:
                                effect="was not very effective."
                if bonus==1:
                                effect="was fine. "
                if bonus==2:
                                effect="was super effective!"
                if bonus==4:
                                effect="was ultra effective!!!!"

                return [bonus,"The attack "+effect]



FirBonus={"Fir":[["Fir",1/2],["Wat",1/2],["Gra",2],["Ice",2],["Bug",2],["Roc",1/2],["Dra",1/2],["Ste",2]]}
NorBonus={"Nor":[["Roc",1/2],["Gho",0],["Ste",1/2]]}
WatBonus={"Wat":[["Fir",2],["Wat",1/2],["Gra",1/2],["Gro",2],["Roc",2],["Dra",1/2]]}
EleBonus={"Ele":[["Wat",2],["Ele",1/2],["Gra",1/2],["Gro",0],["Fly",2],["Dra",1/2]]}
GraBonus={"Gra":[["Fir",1/2],["Wat",2],["Gra",1/2],["Poi",1/2],["Gro",2],["Fly",1/2],["Bug",1/2],["Roc",2],["Dra",1/2],["Ste",1/2]]}
IceBonus={"Ice":[["Fir",1/2],["Wat",1/2],["Grass",2],["Ice",1/2],["Gro",2],["Fly",2],["Dra",2],["Ste",1/2]]}
FigBonus={"Fig":[["Nor",2],["Ice",2],["Poi",1/2],["Fly",1/2],["Roc",1/2],["Gho",0],["Dar",2],["Ste",2],["Fai",1/2]]}
PoiBonus={"Poi":[["Gra",2],["Poi",1/2],["Gro",1/2],["Roc",1/2],["Gho",1/2],["Ste",0],["Fai",2]]}
GroBonus={"Gro":[["Fir",2],["Ele",2],["Gra",1/2],["Poi",2],["Fly",0],["Bug",1/2],["Roc",2],["Ste",2]]}
FlyBonus={"Fly":[["Ele",1/2],["Gra",2],["Fig",2],["Bug",2],["Roc",1/2],["Ste",1/2]]}
PsyBonus={"Psy":[["Fig",2],["Poi",2],["Psy",1/2],["Dar",0],["Ste",1/2]]}
BugBonus={"Bug":[["Fir",1/2],["Gra",2],["Fig",1/2],["Poi",1/2],["Fly",1/2],["Psy",2],["Gho",1/2],["Dar",2],["Ste",1/2],["Fai",1/2]]}
RocBonus={"Roc":[["Fir",2],["Ice",2],["Fig",1/2],["Fly",2],["Gro",1/2],["Bug",2],["Ste",1/2]]}
GhoBonus={"Gho":[["Nor",0],["Psy",2],["Gho",2],["Dar",2],["Ste",1/2]]}
DraBonus={"Dra":[["Dra",2],["Ste",1/2],["Fai",0]]}
DarBonus={"Dar":[["Fig",1/2],["Psy",2],["Gho",2],["Dar",1/2],["Fai",1/2]]}
SteBonus={"Ste":[["Fir",1/2],["Wat",1/2],["Ele",1/2],["Ice",2],["Roc",2],["Ste",1/2],["Fai",2]]}
FaiBonus={"Fai":[["Fir",1/2],["Fig",1/2],["Poi",1/2],["Dra",2],["Dar",2],["Ste",1/2]]}



def PokeName(code):
                return PokeStat[code][0]

def PokeType(code):
                if len(PokeStat[code][1])==1:
                                return PokeStat[code][1]
                if len(PokeStat[code][1])==2:
                                return PokeStat[code][2][0],PokeStat[number][1][1]

def Pokelevel(name):
                for i in range (len(UserPoke)):
                                # print(UserPoke[i][0][0])
                                if UserPoke[i][0][0]==name:
                                                return trunc(UserPoke[i][2][0]/500)


def PokeAtkP(code):
                return PokeStat[number][3][1]

def PokeDefP(code):
                return PokeStat[number][3][1]

def PokeXPCalc(level):
                xp=level*500
                atkGain=level/2
                defGain=level/2
                return [xp,atkGain,defGain]


#Dictionary of 1st-gen Pokemon, with name, type, base stats, attacks
#and evolutionary stats.


PokeStat={1:[['Bulbasaur'],["Gra","Poi"],["A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokémon."],[49,49],["Razor Leaf","Vine Whip","Tackle","Double Edge"],[45],["Ivysaur",16]],
                                  2:[["Ivysaur"],["Gra","Poi"],["When the bulb on its back grows large, it appears to lose the ability to stand on its hind legs."],[62,63],["Vine Whip","Razor Leaf","Mega Drain","Poisonpowder"],[45],["Venasaur",32]],
                                  3:[["Venusaur"],["Gra","Poi"],["The plant blooms when it is absorbing solar energy. It stays on the move to seek sunlight."],[82,83],["Razor Leaf","Giga Drain","Solar Beam","Double Edge"],[45],["Final Stage of Evolution"]],
                                  4:[["Charmander"],["Fir"],["Obviously prefers hot places. When it rains, steam is said to spout from the tip of its tail."],[52,43],["Scratch","Ember","Fire Punch","Tackle"],[45],["Charmeleon",16]],
                                  5:[["Charmeleon"],["Fir"],["When it swings its burning tail, it elevates the temperature to unbearably high levels."],[64,58],["Fire Fang","Flamethrower","Slash","Double Edge"],[45],["Charizard",36]],
                                  6:[["Charizard"],["Fir","Fly"],["It spits fire that is hot enough to melt boulders. Known to cause forest fires unintentionally."],[84,78],["Fire Blast", "Wing Attack", "Flamethrower","Double Edge"],[45],["Final Stage of Evolution"]],
                                  7:[["Squirtle"],["Wat"],["After birth, its back swells and hardens into a shell. Powerful sprays foam from its mouth."],[48,65],["Tackle", "Bubble", "Water Gun","Bite"],[45],["Wartortle",16]],
                                  8:[["Wartortle"],["Wat"],["Often hides in water to stalk unwary prey. For swimming fast, it moves its ears to maintain balance."],[63,80],["Slam", "Water Gun", "Bubblebeam","Crunch"],[45],["Blastoise",36]],
                                  9:[["Blastoise"],["Wat"],["A brutal Pokémon with pressurized water jets on its shell. They are used for high speed tackles."],[83,10],["Hydro Pump","Ice Beam","Crunch","Bubblebeam"],[45],["Final Stage of Evolution"]],
                                  10:[["Caterpie"],["Bug"],["Its short feet are tipped with suction pads that enable it to tirelessly climb slopes and walls."],[30,35],["Tackle","String Shot","Splash","Fury Cutter"],[255],["Metapod",7]],
                                  11:[["Metapod"],["Bug"],["This Pokémon is vulnerable to attack while its shell is soft, exposing its weak and tender body."],[25,50],["Tackle","String Shot","Harden","Splash"],[120],["Butterfree",10]],
                                  12:[["Butterfree"],["Bug","Fly"],["In battle, it flaps its wings at high speed, releasing highly toxic dust into the air."],[45,50],["Psybeam","Gust","Confusion","Silver Wind"],[45],["Final Stage of Evolution"]],
                                  13:[["Weedle"],["Bug","Poi"],["Often found in forests, eating leaves. It has a sharp venomous stinger on its head."],[35,30],["Tackle","String Shot","Splash","Poison Sting"],[255],["Kakuna",7]],
                                  14:[["Kakuna"],["Bug","Poi"],["Almost incapable of moving, this Pokémon can only harden its shell to protect itself from predators."],[25,50],["Tackle","String Shot","Poison Sting","Harden"],[120],["Beedrill",10]],
                                  15:[["Beedrill"],["Bug","Poi"],["Flies at high speed and attacks using its large venomous stingers on its forelegs and tail."],[90,40],["Poison Jab","Silver Wind","Fury Attack","Headbutt"],[45],["Final Stage of Evolution"]],
                                  16:[["Pidgey"],["Fly","Nor"],["A common sight in forests and woods. It flaps its wings at ground level to kick up blinding sand."],[45,40],["Tackle","Gust","Quick Attack","Wing Attack"],[255],["Pidgeotto",18]],
                                  17:[["Pidgeotto"],["Fly","Nor"],["Very protective of its sprawling territory, this Pokémon will fiercely peck at any intruder."],[60,55],["Wing Attack","Quick Attack","Peck","Secret Power"],[120],["Pidgeot",36]],
                                  18:[["Pidgeot"],["Fly","Nor"],["When hunting, it skims the surface of water at high speed to pick off unwary prey such as Magikarp."],[80,75],["Drill Peck","Wing Attack","Secret Power","Hyper Beam"],[45],["Final Stage of Evolution"]],
                                  19:[["Rattata"],["Nor"],["Bites anything when it attacks. Small and very quick, it is a common sight in many places."],[56,35],["Bite","Hyper Fang","Tackle","Quick Attack"],[255],["Raticate",20]],
                                  20:[["Raticate"],["Nor"],["It uses its whiskers to maintain its balance and will slow down if they are cut off."],[81,60],["Super Fang","Hyper Fang","Secret Power","Quick Attack"],[127],["Final Stage of Evolution"]],
                                  21:[["Spearow"],["Nor","Fly"],["Eats bugs in grassy areas. It has to flap its short wings at high speed to stay airborne."],[60,30],["Peck","Wing Attack","Quick Attack","Aerial Ace"],[255],["Fearow",20]],
                                  22:[["Fearow"],["Nor","Fly"],["With its huge and magnificent wings, it can keep aloft without ever having to land for rest."],[90,65],["Drill Peck","Pluck","Quick Attack"],[90],["Final Stage of Evolution"]],
                                  23:[["Ekans"],["Poi"],["Moves silently and stealthily. Eats the eggs of birds, such as Pidgey and Spearow, whole."],[60,44],["Wrap","Poison Sting","Bite","Acid"],[255],["Arbok",22]],
                                  24:[["Arbok"],["Poi"],["It is rumored that the ferocious warning markings on its belly differ from area to area."],[85,69],["Poison Fang","Poison Sting","Wrap","Mud Bomb"],[90],["Final Stage of Evolution"]],
                                  25:[["Pikachu"],["Ele"],["When several of these Pokémon gather, their electricity could build and cause lightning storms."],[55,40],["Thunder Shock","Shock Wave","Quick Attack","Slam"],[190],["Raichu","Thunder Stone"]],
                                  26:[["Raichu"],["Ele"],["Its long tail serves as a ground to protect itself from its own high voltage power."],[90,55],["Thunderbolt","Shock Wave","Slam","Facade"],[75],["Final Stage of Evolution"]],
                                  27:[["Sandshrew"],["Gro"],["Burrows deep underground in arid locations far from water. It only emerges to hunt for food."],[75,85],["Dig","Scratch","Mud Slap","Tackle"],[255],[90],["Sandslash",22]],
                                  28:[["Sandslash"],["Gro"],["Curls up into a spiny ball when threatened. It can roll while curled up to attack or escape."],[100,110],["Dig","Slash","Facade","Quick Attack"],["Final Stage of Evolution"]],
                                  29:[["NidoranF"],["Poi","Gro"],["Although small, its venomous barbs render this Pokémon dangerous. The female has smaller horns."],[47,52],["Poison Sting","Quick Attack","Double Kick","Fury Swipes"],[235],["Nidorina",16]],
                                  30:[["Nidorina"],["Poi","Gro"],["The female's horn develops slowly. Prefers physical attacks such as clawing and biting."],[62,67],["Poison Fang","Poison Sting","Double Kick","Horn Attack"],[120],["Nidoqueen","Moon Stone"]],
                                  31:[["Nidoqueen"],["Poi","Gro"],["Its hard scales provide strong protection. It uses its hefty bulk to execute powerful moves."],[92,87],["Double Kick","Earthquake","Poison Sting","Stomp"],[45],["Final Stage of Evolution","Moon Stone"]],
                                  32:[["NidoranM"],["Poi","Gro"],["Stiffens its ears to sense danger. The larger its horns, the more powerful its secreted venom."],[57,40],["Poison Sting","Horn Attack","Tackle","Dig"],[235],["Nidorino",16]],
                                  33:[["Nidorino"],["Poi","Gro"],["An aggressive Pokémon that is quick to attack. The horn on its head secretes a powerful venom"],[72,57],["Double Kick","Horn Attack","Dig","Take Down"],[120],["Nidoking","Moon Stone"]],
                                  34:[["Nidoking"],["Poi","Gro"],["It uses its powerful tail in battle to smash, constrict, then break the prey's bones."],[102,77],["Earthquake","Megahorn","Horn Attack","Mega Kick"],[45],["Final Stage of Evolution"]],
                                  35:[["Clefairy"],["Fai"],["Its magical and cute appeal has many admirers. It is rare and found only in certain areas."],[45,48],["Double Slap","Pound","Quick Attack","Sing"],[150],["Clefable","Moon Stone"]],
                                  36:[["Clefable"],["Fai"],["A timid fairy Pokémon that is rarely seen. It will run and hide the moment it senses people."],[70,73],["Double Slap","Secret Power","Facade","Sing"],[45],["Final Stage of Evolution"]],
                                  37:[["Vulpix"],["Fir"],["At the time of birth, it has just one tail. The tail splits from its tip as it grows older."],[41,40],["Ember","Confuse Ray","Quick Attack","Leer"],[190],["Ninetales","Fire Stone"]],
                                  38:[["Ninetales"],["Fir"],["Very smart and very vengeful. Grabbing one of its many tails could result in a 1000-year curse."],[76,75],["Flamethrower","Confuse Ray","Screech","Fire Spin"],[75],["Final Stage of Evolution"]],
                                  39:[["Jigglypuff"],["Nor","Fai"],["When its huge eyes light up, it sings a mysteriously soothing melody that lulls its enemies to sleep."],[45,20],["Sing","Pound","Double Slap","Secret Power"],[170],["Wigglytuff","Moon Stone"]],
                                  40:[["Wigglytuff"],["Nor","Fai"],["The body is soft and rubbery. When angered, it will suck in air and inflate itself to an enormous size."],[70,45],["Sing","Double Slap","Facade","Tackle"],[50],["Final Stage of Evolution"]],
                                  41:[["Zubat"],["Poi","Fly"],["Forms colonies in perpetually dark places. Uses ultrasonic waves to identify and approach targets."],[45,35],["Confuse Ray","Wing Attack","Leech Life","Tackle"],[255],["Golbat",22]],
                                  42:[["Golbat"],["Poi","Fly"],["Once it strikes, it will not stop draining energy from the victim even if it gets too heavy to fly."],[80,70],["Confuse Ray","Air Cutter","Wing Attack","Poison Fang"],[90],["Final Stage of Evolution"]],

                                  43:[["Oddish"],["Gra","Poi"],["During the day, it keeps its face buried in the ground. At night, it wanders around sowing its seeds."],[50,55],["Sleep Powder","Poisonpowder","Absorb","Pound"],[255],["Gloom",21]],
                                  44:[["Gloom"],["Gra","Poi"],["The fluid that oozes from its mouth isn't drool. It's a nectar that is used to attract prey."],[65,70],["Sleep Powder","Mega Drain","Absorb","Slam"],[120],["Vineplume","Leaf Stone"]],
                                  45:[["Vineplume"],["Gra","Poi"],["The larger its petals, the more toxic pollen it contains. Its big head is heavy and hard to hold up."],[80,85],["Giga Drain","Acid","Slam","Sleep Powder"],[45],["Final Stage of Evolution"]],
                                  46:[["Paras"],["Gra","Bug"],["Burrows to suck tree roots. The mushrooms on its back grow by drawing nutrients from the bug host."],[70,55],["Scratch","Fury Cutter","Tackle","Leech Life"],[190],["Parasect",24]],
                                  47:[["Parasect"],["Gra","Bug"],["A host-parasite pair in which the parasite mushroom has taken over the host bug. Prefers damp places."],[95,80],["Fury Cutter","Signal Beam","Cut","Slash"],[75],["Final Stage of Evolution"]],
                                  48:[["Venonat"],["Poi","Bug"],["Lives in the shadows of tall trees where it eats bugs. It is attracted by light at night"],[55,50],["Poisonpowder","Tackle","Acid","Confusion"],[190],["Venomoth",31]],
                                  49:[["Venomoth"],["Poi","Bug"],["The dust-like scales covering its wings are color coded to indicate the kinds of poison it has."],[65,60],["Wing Attack","Silver Wind","Acid","Signal Beam"],[75],["Final Stage of Evolution"]],
                                  50:[["Diglett"],["Gro"],["Lives about one yard underground where it feeds on plant roots. It sometimes appears above ground."],[55,25],["Dig","Scratch","Leer","Quick Attack"],[255],["Dugtrio",26]],
                                  51:[["Dugtrio"],["Gro"],["A team of Diglett triplets. It triggers huge earthquakes by burrowing 60 miles underground."],[80,50],["Dig","Slash","Slam","Earth Power"],[50],["Final Stage of Evolution"]],
                                  52:[["Meowth"],["Nor"],["Adores circular objects. Wanders the street on a nightly basis to look for dropped loose change."],[45,35],["Scratch","Quick Attack","Growl","Pay Day"],[255],["Persian",28]],
                                  53:[["Persian"],["Nor"],["Although its fur has many admirers, it is tough to raise as a pet because of its fickle meanness."],[70,60],["Slash","Secret Power","Pay Day","Screech"],[90],["Final Stage of Evolution"]],
                                  54:[["Psyduck"],["Wat"],["While lulling its enemies with its vacant look, this wily Pokémon will use psychokinetic powers."],[52,48],["Confusion","Water Gun","Scratch","Confuse Ray"],["Golduck",33]],
                                  55:[["Golduck"],["Wat"],["Often seen swimming elegantly by lakeshores. It is often mistaken for the Japanese monster Kappa."],[82,78],["Confusion","Bubblebeam","Slash","Brine"],[190],[75],["Final Stage of Evolution"]],
                                  56:[["Mankey"],["Fig"],["Extremely quick to anger. It could be docile one moment then thrashing away the next instant."],[80,35],["Low Kick","Scratch","Thrash","Karate Chop"],[190],["Primeape",28]],
                                  57:[["Primeape"],["Fig"],["Always furious and tenacious to boot. It will not abandon chasing its quarry until it is caught."],[105,60],["Cross Chop","Brick Break","Scratch","Leer"],[75],["Final Stage of Evolution"]],
                                  58:[["Growlithe"],["Fir"],["Very protective of its territory. It will bark and bite to repel intruders from its space."],[70,45],["Ember","Quick Attack","Flame Wheel","Growl"],[190],["Arcanine","Fire Stone"]],
                                  59:[["Arcanine"],["Fir"],["A Pokémon that has been admired since the past for its beauty. It runs agilely as if on wings."],[110,80],["Flame Wheel","Flamethrower","Extremespeed","Screech"],[75],["Final Stage of Evolution"]],
                                  60:[["Poliwag"],["Wat"],["Its newly grown legs prevent it from walking well. It appears to prefer swimming over walking."],[50,40],["Bubble","Water Gun","Hypnosis","Pound"],[255],["Poliwhirl",25]],
                                  61:[["Poliwhirl"],["Wat"],["It can live in or out of water. When out of water, it constantly sweats to keep its body slimy."],[65,65],["Bubblebeam","Water Gun","Hypnosis","Slam"],[120],["Poliwrath","Water Stone"]],
                                  62:[["Poliwrath"],["Wat","Fig"],["A graradept at both the front crawl and breaststroke. Easily overtakes the best human swimmers."],[95,95],["Surf","Mega Punch","Water Gun","Hypnosis"],[45],["Final Stage of Evolution"]],
                                  63:[["Abra"],["Psy"],["Using its ability to read minds, it will sense impending danger and teleport to safety."],[20,15],["Confusion","Teleport","Scratch","Psywave"],[200],["Kadabra",16]],
                                  64:[["Kadabra"],["Psy"],["It emits special alpha waves from its body that induce headaches just by being close by."],[35,30],["Confusion","Psybeam","Psywave","Thunder Shock"],[100],["Alakazam",32]],
                                  65:[["Alakazam"],["Psy"],["Its brain can outperform a super-computer. Its intelligence quotient is said to be 5,000."],[50,45],["Psychic","Psybeam","Thunderbolt","Calm Mind"],[50],["Final Stage of Evolution"]],
                                  66:[["Machop"],["Fig"],["oves to build its muscles. It trains in all styles of martial arts to become even stronger."],[80,50],["Karate Chop","Low Kick","Comet Punch","Body Slam"],[180],["Machoke",28]],
                                  67:[["Machoke"],["Fig"],["Its muscular body is so powerful, it must wear a power-save belt to be able to regulate its motions."],[100,70],["Karate Chop","Body Slam","Mach Punch","Fire Punch"],[90],["Machamp",40]],
                                  68:[["Machamp"],["Fig"],["Using its heavy muscles, it throws powerful punches that can send the victim clear over the horizon."],[130,80],["Cross Chop","Seismic Toss","Fire Punch","Thunder Punch"],[45],["Final Stage of Evolution"]],
                                  69:[["Bellsprout"],["Gra","Poi"],["A carnivorous Pokémon that traps and eats bugs. It appears to use its root feet to replenish moisture."],[75,35],["Vine Whip","Absorb","Wrap","Bind"],[255],["Weepinbell",21]],
                                  70:[["Weepinbell"],["Gra","Poi"],["It spits out poisonpowder to immobilize the enemy and then finishes it with a spray of acid."],[90,50],["Vine Whip","Razor Leaf","Sleep Powder","Acid"],[120],["Victreebel","Leaf Stone"]],
                                  71:[["Victreebel"],["Gra","Poi"],["Said to live in huge colonies deep in jungles, although no one has ever returned from there."],[105,65],["Razor Leaf","Acid","Sludge","Solar Beam"],[45],["Final Stage of Evolution"]],
                                  72:[["Tentacool"],["Wat","Poi"],["Drifts in shallow seas. Anglers who hook them by accident are often punished by its stinging acid."],[40,35],["Acid","Water Gun","Constrict","Wrap"],[190],["Tentacruel",30]],
                                  73:[["Tentacruel"],["Wat","Poi"],["The tentacles are normally kept short. On hunts, they are extended to ensnare and immobilize prey."],[70,65],["Acid","Bubblebeam","Sludge","Constrict"],[60],["Final Stage of Evolution"]],
                                  74:[["Geodude"],["Roc","Gro"],["Found in fields and mountains. Mistaking them for boulders, people often step or trip on them."],[80,100],["Rock Throw","Magnitude","Tackle","Rollout"],[255],["Graveler",25]],
                                  75:[["Graveler"],["Roc","Gro"],["Rolls down slopes to move. It rolls over any obstacle without slowing or changing its direction."],[95,115],["Rock Throw","Magnitude","Slam","Harden"],[120],["Golem",35]],
                                  76:[["Golem"],["Roc","Gro"],["Its boulder-like body is extremely hard. It can easily withstand dynamite blasts without taking damage."],[120,130],["Earth Power","Rock Slide","Dig","Rollout"],[45],["Final Stage of Evolution"]],
                                  77:[["Ponyta"],["Fir"],["Its hooves are 10 times harder than diamonds. It can trample anything completely flat in little time."],[85,55],["Ember","Fire Spin","Stomp","Quick Attack"],[190],["Rapidash",40]],
                                  78:[["Rapidash"],["Fir"],["Very competitive, this Pokémon will chase anything that moves fast in the hopes of racing it."],[100,70],["Stomp","Fire Spin","Flame Wheel","Extremespeed"],[60],["Final Stage of Evolution"]],
                                  79:[["Slowpoke"],["Wat","Psy"],["Incredibly slow and dopey. It takes 5 seconds for it to feel pain when under attack."],[65,65],["Confusion","Water Gun","Tail Whip","Bubble"],[190],["Slowbro",37]],
                                  80:[["Slowbro"],["Wat","Psy"],["The Shellder that latches onto Slowpoke's tail is said to feed on the host's leftover scraps."],[75,110],["Confusion","Water Gun","Bubble","Confuse Ray"],[75],["Final Stage of Evolution"]],

                                  81:[["Magnemite"],["Ele","Ste"],["Uses antigravity to stay suspended. Appears without warning and uses Thunder Wave and similar moves."],[35,70],["Thunder Shock","Tackle","Thunder Wave","Sonicboom"],[190],["Magneton",30]],
                                  82:[["Magneton"],["Ele","Ste"],["Formed by several Magnemite linked together. They frequently appear when sunspots flare up."],[60,95],["Thunderbolt","Sonicboom","Mirror Shot","Magnet Bomb"],[60],["Final Stage of Evolution"]],
                                  83:[["Farfetch'd"],["Fly","Nor"],["The spring of green onions it holds is its weapon. It is used much like a metal sword."],[65,55],["Wing Attack","Quick Attack","Cut","False Swipe"],[45],["Final Stage of Evolution"]],
                                  84:[["Doduo"],["Fly","Nor"],["A bird that makes up for its poor flying with its fast foot speed. Leaves giant footprints."],[110,70],["Peck","Fury Attack","Stomp","Quick Attack"],[190],["Dodrio",31]],
                                  85:[["Dodrio"],["Fly","Nor"],["It uses three brains to execute complex plans. While two heads sleep, one head is said to stay awake."],[110,70],['Drill Peck','Peck','Extremespeed','Stomp'],[45],["Final Stage of Evolution"]],
                                  86:[["Seel"],["Wat","Ice"],["The protruding horn on its head is very hard. It is used for bashing through thick ice."],[45,55],["Aurora Beam",'Water Gun','Body Slam','Powder Snow'],[190],["Dewgong",34]],
                                  87:[["Dewgong"],["Wat","Ice"],["Stores thermal energy in its body. Swims at a steady 8 knots even in intensely cold waters."],[70,80],["Surf","Ice Beam","Body Slam","Aqua Tail"],[75],["Final Stage of Evolution"]],
                                  88:[["Grimer"],["Poi"],["Appears in filthy areas. Thrives by sucking up polluted sludge that is pumped out of factories."],[80,50],["Tackle","Poison Gas","Mud Slap","Sludge"],[190],["Muk",38]],
                                  89:[["Muk"],["Poi"],["Thickly covered with a filthy, vile sludge. It is so toxic, even its footprints contain poison."],[105,75],["Sludge","Sludge Bomb","Pound","Toxic"],[75],["Final Stage of Evolution"]],
                                  90:[["Shellder"],["Wat","Ice"],["Its hard shell repels any kind of attack. It is vulnerable only when its shell is open."],[65,100],["Aurora Beam","Water Gun","Splash","Tackle"],[190],["Cloyster","Water Stone"]],
                                  91:[["Cloyster"],["Wat","Ice"],["When attacked, it launches its horns in quick volleys. Its innards have never been seen."],[95,180],["Water Gun","Aurora Beam","Ice Beam","Spike Cannon"],[60],["Final Stage of Evolution"]],
                                  92:[["Gastly"],["Gho","Poi"],["Almost invisible, this gaseous Pokémon cloaks the target and puts it to sleep without notice."],[35,30],["Lick","Hypnosis","Night Shade","Confuse Ray"],[190],["Haunter",25]],
                                  93:[["Haunter"],["Gho","Poi"],["Because of its ability to slip through block walls, it is said to be from another dimension."],[50,45],["Hypnosis","Poison Gas","Shadow Ball","Sucker Punch"],[90],["Gengar",40]],
                                  94:[["Gengar"],["Gho","Poi"],["Under a full moon, this Pokémon likes to mimic the shadows of people and laugh at their fright."],[65,60],["Hypnosis","Sludge Bomb","Shadow Ball","Sucker Punch"],[45],["Final Stage of Evolution"]],
                                  95:[["Onix"],["Roc","Gro"],["As it grows, the stone portions of its body harden to become similar to a diamond, but colored black."],[45,160],["Bind","Rock Throw","Slam","Rock Tomb"],[45],["Final Stage of Evolution"]],
                                  96:[["Drowzee"],["Psy"],["Puts enemies to sleep then eats their dreams. Occasionally gets sick from eating bad dreams."],[48,45],["Confusion","Hypnosis","Pound","Body Slam"],[190],["Hypno", 26]],
                                  97:[["Hypno"],["Psy"],["When it locks eyes with an enemy, it will use a mix of PSI moves such as Hypnosis and Confusion."],[73,70],["Psychic","Headbutt","Zen Headbutt","Psybeam"],[75],["Final Stage of Evolution"]],
                                  98:[["Krabby"],["Wat"],["Its pincers are not only powerful weapons, they are used for balance when walking sideways."],[105,90],["Water Gun","Vicegrip","Cut","Bubble"],[225],["Kingler",28]],
                                  99:[["Kingler"],["Wat"],["The large pincer has 10,000-horsepower crushing force. However, its huge size makes it unwieldy to use."],[130,115],["Bubblebeam","Crabhammer","Vicegrip","Metal Claw"],[60],["Final Stage of Evolution"]],
                                  100:[["Voltorb"],["Ele"],["Usually found in power plants. Easily mistaken for a Poké Ball, it has zapped many people."],[50,70],["Sonicboom","Explosion","Spark","Rollout"],[190],["Electrode",30]],
                                  101:[["Electrode"],["Ele"],["It stores electric energy under very high pressure. It often explodes with little or no provocation."],[50,70],["Explosion","Spark","Thunderbolt","Charge Beam"],[60],["Final Stage of Evolution"]],
                                  102:[["Exeggcute"],["Gra"],["It is often mistaken for eggs. When disturbed, they gather quickly and attack in swarms."],[40,80],["Uproar","Bullet Seed","Sleep Powder","Confusion"],[90],["Exeggutor","Leaf Stone"]],
                                  103:[["Exeggutor"],["Gra"],["Legend has it that on rare occasions, one of its heads will drop off and continue on as an Exeggcute."],[95,85],["Hypnosis","Confusion","Psychic","Razor Leaf"],[45],["Final Stage of Evolution"]],
                                  104:[["Cubone"],["Gro"],["Because it never removes its skull helmet, no one has ever seen this Pokémon's real face."],[50,95],["Headbutt","Bone Club","Bonemerang","False Swipe"],[190],["Marowak",28]],
                                  105:[["Marowak"],["Gro"],["The bone it holds is its key weapon. It throws the bone skillfully like a boomerang to KO targets."],[80,110],["Bonemerang","Headbutt","Thrash","Dig"],[75],["Final Stage of Evolution"]],
                                  106:[["Hitmonlee"],["Fig"],["When in a hurry, its legs lengthen progressively. It runs smoothly with extra long, loping strides."],[120,53],["Double Kick","Rolling Kick","Jump Kick","Brick Break"],[45],["Final Stage of Evolution"]],
                                  107:[["Hitmonchan"],["Fig"],["While apparently doing nothing, it fires punches in lightning fast volleys that are impossible to see."],[105,79],["Ice Punch","Mach Punch","Thunder Punch","Fire Punch"],[45],["Final Stage of Evolution"]],
                                  108:[["Lickitung"],["Nor"],["Its tongue can be extended like a chameleon's. It leaves a tingling sensation when it licks enemies."],[55,75],["Rollout","Lick","Secret Power","Wrap"],[45],["Final Stage of Evolution"]],
                                  109:[["Koffing"],["Poi"],["Because it stores several kinds of toxic gases in its body, it is prone to exploding without warning."],[65,95],["Poison Gas","Smog","Sludge","Assurance"],[190],["Weezing",34]],
                                  110:[["Weezing"],["Poi"],["Where two kinds of poison gases meet, two Koffings can fuse into a Weezing over many years."],[90,120],["Sludge","Poison Gas","Smog","Smokescreen"],[60],["Final Stage of Evolution"]],
                                  111:[["Rhyhorn"],["Gro","Roc"],["Its massive bones are 1000 times harder than human bones. It can easily knock a trailer flying."],[85,90],["Horn Attack","Rock Throw","Take Down","Rock Blast"],[60],["Rhydon",42]],
                                  112:[["Rhydon"],["Gro","Roc"],["Protected by an armor-like hide, it is capable of living in molten lava of 3,600 degrees."],[130,120],["Stone Edge","Megahorn","Rock Blast","Stomp"],[120],["Final Stage of Evolution"]],
                                  113:[["Chansey"],["Nor"],["A rare and elusive Pokémon that is said to bring happiness to those who manage to get it."],[5,5],["Pound","Softboiled","Double Slap","Sing"],["Final Stage of Evolution"]],
                                  114:[["Tangla"],["Gra"],["The whole body is swathed with wide vines that are similar to seaweed. The vines sway as it walks."],[55,115],["Ancient Power","Vine Whip","Absorb","Pound"],[45],["Final Stage of Evolution"]],
                                  115:[["Kangaskhan"],["Nor"],["The infant rarely ventures out of its mother's protective pouch until it is 3 years old."],[95,80],["Comet Punch","Fake Out","Bite","Mega Punch"],[45],["Final Stage of Evolution"]],

                                  116:[["Horsea"],["Wat"],["Known to shoot down flying bugs with precision blasts of ink from the surface of the water."],[40,70],["Water Gun","Bubble","Pound","Twister"],[225],["Horsea",32]],
                                  117:[["Seadra"],["Wat"],["Capable of swimming backwards by rapidly flapping its wing-like pectoral fins and stout tail."],[65,95],["Bubblebeam","Dragon Rage","Leer","Water Gun"],[75],["Final Stage of Evolution"]],
                                  118:[["Goldeen"],["Wat"],["Its tail fin billows like an elegant ballroom dress, giving it the nickname of the Water Queen."],[67,60],["Bubble","Pound","Horn Attack","Water Gun"],[225],["Seeking",33]],
                                  119:[["Seaking"],["Wat"],["In the autumn spawning season, they can be seen swimming powerfully up rivers and creeks."],[92,65],["Drill Peck","Horn Attack","Surf","Bubble"],[85,90],["Final Stage of Evolution"]],
                                  120:[["Staryu"],["Wat","Psy"],["An enigmatic Pokémon that can regenerate any appendage it loses in battle."],[45,55],["Water Gun","Rapid Spin","Bubble","Slam",],[225],["Starmie","Water Stone"]],
                                  121:[["Starmie"],["Wat","Psy"],["Its central core glows with the seven colors of the rainbow. Some people value the core as a gem."],[75,85],["Rapid Spin","Surf","Aurora Beam","Confusion"],[60],["Final Stage of Evolution"]],
                                  122:[["Mr.Mime"],["Fai","Psy"],["If interrupted while it is miming, it will slap around the offender with its broad hands."],[45,65],["Confusion","Pound","Double Slap","Psychic"],[45],["Final Stage of Evolution"]],
                                  123:[["Scyther"],["Bug","Fly"],["With ninja-like agility and speed, it can create the illusion that there is more than one."],[45,65],["Slash","Fury Cutter","False Swipe","Wing Attack"],[45],["Final Stage of Evolution"]],
                                  124:[["Jynx"],["Psy","Ice"],["It seductively wiggles its hips as it walks. It can cause people to dance in unison with it."],[50,35],["Confusion","Ice Punch","Lovely Kiss","Powder Snow"],[45],["Final Stage of Evolution"]],
                                  125:[["Elecabuzz"],["Ele"],["Normally found near power plants, they can wander away and cause major blackouts in cities."],[83,57],["Thunder Punch","Quick Attack","Take Down","Shock Wave"],[45],["Final Stage of Evolution"]],
                                  126:[["Magmar"],["Fir"],["Its body always burns with an orange glow that enables it to hide perfectly among flames."],[95,57],["Fire Punch","Smog","Ember","Mega Punch"],[45],["Final Stage of Evolution"]],
                                  127:[["Pinsir"],["Bug"],["If it fails to crush the victim in its pincers, it will swing it around and toss it hard."],[120,100],["Vicegrip","Bind","Brick Break","Cut"],[45],["Final Stage of Evolution"]],
                                  128:[["Tauros"],["Nor"],["When it targets an enemy, it charges furiously while whipping its body with its long tails."],[100,95],["Stomp","Take Down","Mud Shot","Horn Attack"],[45],["Final Stage of Evolution"]],
                                  129:[["Magikarp"],["Wat"],["In the distant past, it was somewhat stronger than the horribly weak descendants that exist today."],[10,55],["Splash","Tackle","Splash","Splash"],[255],["Gyarados",20]],
                                  130:[["Gyarados"],["Wat","Fly"],["Rarely seen in the wild. Huge and vicious, it is capable of destroying entire cities in a rage."],[155,109],["Waterfall","Thrash",'Aerial Ace',"Water Pulse"],[45],["Final Stage of Evolution"]],
                                  131:[["Lapras"],["Wat","Ice"],["A Pokémon that has been overhunted almost to extinction. It can ferry people across the water."],[85,80],["Ice Beam","Surf","Water Gun","Confuse Ray"],["Final Stage of Evolution"]],
                                  132:[["Ditto"],["Nor"],["Capable of copying an enemy's genetic code to instantly transform itself into a duplicate of the enemy."],[48,48],["Pound","Tackle","Slam","Secret Power"],["Final Stage of Evolution"]],
                                  133:[["Eevee"],["Nor"],["Its genetic code is irregular. It may mutate if it is exposed to radiation from element stones."],[55,50],["Quick Attack","Secret Power","Iron Tail","Tackle"],[45],[["Vaporeon","Water Stone"],["Flareon","Fire Stone"],["Jolteon","Thunder Stone"]]],
                                  134:[["Vaporeon"],["Wat"],["Lives close to water. Its long tail is ridged with a fin which is often mistaken for a mermaid's."],[65,60],["Aurora Beam","Water Gun","Aqua Tail","Bubblebeam"],[45],["Final Stage of Evolution"]],
                                  135:[["Jolteon"],["Ele"],["It accumulates negative ions in the atmosphere to blast out 10000-volt lightning bolts."],[65,60],["Thunder Shock","Quick Attack","Shock Wave","Thunder Fang"],[45],["Final Stage of Evolution"]],
                                  136:[["Flareon"],["Fir"],["When storing thermal energy in its body, its temperature could soar to over 1,600 degrees."],[130,60],["Ember","Quick Attack","Flame Wheel","Fire Spin"],[45],["Final Stage of Evolution"]],
                                  137:[["Porygon"],["Nor"],["A Pokémon that consists entirely of programming code. Capable of moving freely in cyberspace."],[60,70],["Confusion","Signal Beam","Tackle","Rapid Spin"],[45],["Final Stage of Evolution"]],
                                  138:[["Omanyte"],["Roc","Wat"],["Although long extinct, in rare cases, it can be genetically resurrected from fossils."],[40,100],["Rock Blast","Water Gun","Rock Throw","Bubble"],[45],["Omastar",40]],
                                  139:[["Omastar"],["Roc","Wat"],["A prehistoric Pokémon that died out when its heavy shell made it impossible to catch prey."],[60,125],["Brine","Mud Shot","Rock Blast","Ancient Power"],[45],["Final Stage of Evolution"]],
                                  140:[["Kabuto"],["Roc","Wat"],["A Pokémon that was resurrected from a fossil found in what was once the ocean floor eons ago."],[80,90],["Rock Blast","Water Gun","Scratch","Leech Life"],[45],["Kabutops",40]],
                                  141:[["Kabutops"],["Roc","Wat"],["Its sleek shape is perfect for swimming. It slashes prey with its claws and drains the body fluids."],[115,105],["Slash","Rock Slide","Water Gun","False Swipe"],[45],["Final Stage of Evolution"]],
                                  142:[["Aerodactyl"],["Roc","Fly"],["A ferocious, prehistoric Pokémon that goes for the enemy's throat with its serrated saw-like fangs."],[105,65],["Rock Slide","Air Cutter","Aerial Ace","Crunch"],[45],["Final Stage of Evolution"]],
                                  143:[["Snorlax"],["Nor"],["Very lazy. Just eats and sleeps. As its rotund bulk builds, it becomes steadily more slothful."],[110,65],["Rest","Body Slam","Rollout","Crunch"],[25],["Final Stage of Evolution"]],
                                  144:[["Articuno"],["Fly","Ice"],["A legendary bird Pokémon said to appear to doomed people who are lost in icy mountains."],[85,100],["Ice Beam","Sky Attack","Blizzard","Confuse Ray"],[3],["Final Stage of Evolution"]],
                                  145:[["Zapdos"],["Fly","Ele"],["A legendary bird Pokémon that is said to appear from clouds while dropping enormous lightning bolts."],[90,85],["Zap Cannon","Thunderbolt","Drill Peck","Discharge"][3],["Final Stage of Evolution"]],
                                  146:[["Moltres"],["Fly","Fir"],["Known as the legendary bird of fire. Every flap of its wings creates a giant dazzle of flashing flames."],[100,90],["Flamethrower","Sky Attack","Solar Beam","Heat Wave"],[3],["Final Stage of Evolution"]],
                                  147:[["Dratini"],["Dra"],["Long considered a mythical Pokémon until recently, when a small colony was found living underwater."],[64,45],["Wrap","Thunder Wave","Twister","Dragon Rage"],[45],["Dragonair",30]],
                                  148:[["Dragonair"],["Dra"],["A mystical Pokémon that exudes a gentle aura. Has the ability to change climate conditions."],[84,65],["Dragon Rage","Aqua Tail","Twister","Constrict"],[45],["Dragonite",55]],
                                  149:[["Dragonite"],["Dra","Fly"],["An extremely rarely seen marine Pokémon. Its intelligence is said to match that of humans."],[134,95],["Dragon Rage","Dragon Claw","Hyper Beam","Aqua Tail"],[45],["Final Stage of Evolution"]],

                                  150:[["Mewtwo"],["Psy"],["It was created by a scientist after years of horrific gene splicing and DNA engineering experiments."],[110,90],["Psychic","Swift","Psycho Cut","Aura Sphere"],["Final Stage of Evolution"]],
                                  151:[["Mew"],["Psy"],["So rare that it is still said to be a mirage by many experts. Only a few people have seen it worldwide."],[100,100],["Psychic","Flamethrower","Thunder","Ice Beam"],["Final Stage of Evolution"]]}

def getPokeLore(pokeID):
        return PokeStat[pokeID][2][0]


#Dictionary of Attacks, Attack Type, power, pp, and bonus skills
#pp is times the said attack can be reused.

attack={
                                "Bug Bite":[["Bug"],[[60],[100],[20]],[None]],
                                "Hard Roller":[["Bug"],[[55],[95],[25]],[None]],
                                "X-Scissor":[["Bug"],[[80],[100],[15]],[None]],
                                "Leech Life ":[["Bug"],[[20],[100],[15]],[None]],
                                "Pin Missile":[["Bug"],[[[25],[85],[20]]],[None]],
                                "Fury Cutter":[["Bug"],[[40],[95],[20]],[None]],
                                "String Shot":[["Bug"],[[25],[95],[40]],[None]],
                                "Megahorn":[["Bug"],[[120],[85],[10]],[None]],
                                "Silver Wind":[["Bug"],[[60],[100],[5]],[None]],
                                "Signal Beam":[["Bug"],[[75],[100],[15]],["Confuse",1/10]],
                                "Bug Buzz":[["Bug"],[[90],[100],[10]],[None]],

                                "Crunch":[["Dar"],[[80],[100],[15]],[None]],
                                "Dark Pulse":[["Dar"],[[60],[100],[20]],[None]],
                                "Beat Up":[["Dar"],[[50],[90],[20]],[None]],
                                "Fake Out":[["Dar"],[[40],[100],[10]],[None]],
                                "Payback":[["Dar"],[[50],[100],[10]],[None]],
                                "Persuit":[["Dar"],[[60],[100],[20]],[None]],
                                "Sucker Punch":[["Dar"],[[80],[100],[5]],[None]],
                                "Assurance":[["Dar"],[[60],[100],[10]],[None]],
                                "Bite":[["Dar"],[[60],[100],[25]],[None]],

                                "Draco Meteor":[["Dra"],[[130],[90],[5]],[None]],
                                "Dragon Rage":[["Dra"],[[50],[100],[10]],[None]],
                                "Dragon Tail":[["Dra"],[[60],[90],[10]],[None]],
                                "Dragon Claw":[["Dra"],[[80],[100],[15]],[None]],
                                "Outrage":[["Dra"],[[120],[100],[10]],[None]],
                                "Dragon Breath":[["Dra"],[[60],[100],[20]],["Para",3/10]],
                                "Dragon Pulse":[["Dra"],[[85],[100],[10]],[None]],
                                "Dragon Rush ":[["Dra"],[[100],[75],[10]],[None]],
                                "Twister":[["Dra"],[[50],[90],[20]],[None]],

                                "Discharge":[["Ele"],[[80],[100],[15]],["Para",3/10]],
                                "Electro Ball":[["Ele"],[[60],[100],[20]],[None]],
                                "Zap Cannon":[["Ele"],[[120],[50],[5]],["Para",1]],
                                "Thunder":[["Ele"],[[110],[70],[10]],["Para",3/10]],
                                "Electro Web":[["Ele"],[[55],[95],[15]],[None]],
                                "Thunder Wave":[["Ele"],[[0],[100],[20]],["Para",1]],
                                "Bolt Strike":[["Ele"],[[130],[85],[5]],["Para",2/5]],
                                "Thunder Shock":[["Ele"],[[40],[100],[30]],["Para",1/10]],
                                "Shock Wave":[["Ele"],[[65],[95],[15]],[["Para",1/10]]],
                                "Thunder Fang":[["Ele"],[[90],[100],[15]],[None]],
                                "Spark":[["Ele"],[[65],[100],[20]],["Para",3/10]],
                                "Charge Beam":[["Ele"],[[50],[90],[10]],[None]],
                                "Volt Tackle":[["Ele"],[[120],[100],[15]],["Para",1/10]],
                                "Thunder Punch":[["Ele"],[[75],[100],[15]],["Para",1/10]],
                                "Thunderbolt":[["Ele"],[[90],[100],[15]],["Para",1/10]],

                                "Triple Kick":[["Fig"],[[40],[90],[10]],[None]],
                                "Seismic Toss":[["Fig"],[[0],[100],[20]],[None]],
                                "Cross Chop":[["Fig"],[[100],[80],[5]],["HighCrit",1]],
                                "Rolling Kick":[["Fig"],[[60],[85],[15]],["Para",3/10]],
                                "Jump Kick":[["Fig"],[[40],[90],[10]],[None]],
                                "Aura Sphere":[["Fig"],[[80],[100],[20]],[None]],
                                "Mach Punch":[["Fig"],[[40],[100],[30]],[None]],
                                "Dynamic Punch":[["Fig"],[[100],[50],[5]],["Confuse",1]],
                                "Hammer Arm":[["Fig"],[[100],[90],[10]],[None]],
                                "Focus Punch":[["Fig"],[[60],[100],[10]],[None]],
                                "Revenge":[["Fig"],[[40],[90],[10]],[None]],
                                "Drain Punch":[["Fig"],[[75],[100],[10]],[None]],
                                "Sky Uppercut":[["Fig"],[[85],[90],[15]],[None]],
                                "Superpower":[["Fig"],[[120],[100],[5]],[None]],
                                "Force Palm":[["Fig"],[[60],[100],[10]],["Para",3/10]],
                                "Brick Break":[["Fig"],[[75],[100],[15]],[None]],
                                "Sacred Sword":[["Fig"],[[90],[100],[20]],[None]],
                                "Karate Chop":[["Fig"],[[50],[100],[25]],["HighCrit",1]],
                                "Double Kick":[["Fig"],[[30],[100],[30]],[None]],

                                "Fire Fang":[["Fir"],[[65],[95],[15]],["Burn",1/10]],
                                "Flare Blitz":[["Fir"],[[120],[100],[15]],["Burn",1/10]],
                                "Incinerate":[["Fir"],[[60],[100],[15]],[None]],
                                "Flame Wheel":[["Fir"],[[60],[100],[25]],["Burn",1/10]],
                                "Flamethrower":[["Fir"],[[90],[100],[15]],["Burn",1/10]],
                                "Flame Burst":[["Fir"],[[70],[100],[15]],[None]],
                                "Fire Blast":[["Fir"],[[110],[85],[5]],["Burn",1/10]],
                                "Eruption":[["Fir"],[[150],[100],[5]],[None]],
                                "Lava Plume":[["Fir"],[[80],[100],[15]],["Burn",3/10]],
                                "Fire Punch":[["Fir"],[[75],[100],[15]],["Burn",1/10]],
                                "Sacred Fire":[["Fir"],[[100],[90],[10]],[None]],
                                "Overheat":[["Fir"],[[40],[95],[5]],["Burn",1/2]],
                                "Blue Flare":[["Fir"],[[130],[85],[5]],["Burn",1/5]],
                                "Heat Wave":[["Fir"],[[95],[90],[10]],["Burn",1/10]],
                                "Fire Spin":[["Fir"],[[35],[85],[15]],[None]],
                                "Ember":[["Fir"],[[40],[100],[25]],["Burn",1/10]],

                                "Air Cutter":[["Fly"],[[60],[95],[25]],[None]],
                                "Acrobatics":[["Fly"],[[55],[100],[15]],[None]],
                                "Gust":[["Fly"],[[40],[100],[35]],[None]],
                                "Bounce":[["Fly"],[[85],[85],[5]],["Para",3/10],[None]],
                                "Pluck":[["Fly"],[[60],[100],[20]],[None]],
                                "Brave Bird":[["Fly"],[[120],[100],[15]],[None]],
                                "Peck":[["Fly"],[[35],[100],[35]],[None]],
                                "Wing Attack":[["Fly"],[[60],[100],[35]],[None]],
                                "Sky Attack":[["Fly"],[[140],[90],[5]],[None]],
                                "Drill Peck":[["Fly"],[[80],[100],[20]],[None]],
                                "Fly":[["Fly"],[[90],[95],[15]],[None]],
                                "Air Slash":[["Fly"],[[75],[95],[20]],[None]],
                                "Aeroblast":[["Fly"],[[100],[95],[5]],[None]],
                                "Aerial Ace":[["Fly"],[[60],[100],[20]],["HighCrit",1]],

                                "Hypnosis":[["Gho"],[[0],[60],[20]],["Sleep",1]],
                                "Confuse Ray":[["Gho"],[[0],[100],[10]],["Confuse",1]],
                                "Shadow Punch":[["Gho"],[[60],[100],[20]],[None]],
                                "Shadow Ball":[["Gho"],[[80],[100],[15]],[None]],
                                "Night Shade":[["Gho"],[[0],[100],[15]],[None]],
                                "Ominous Wind":[["Gho"],[[60],[100],[5]],["AllRaise",1/10]],
                                "Lick":[["Gho"],[[30],[100],[30]],["Para",3/10]],
                                "Astonish":[["Gho"],[[30],[100],[15]],[None]],
                                "Shadow Sneak":[["Gho"],[[40],[100],[30]],[None]],
                                "Evil Eye":[["Gho"],[[80],[100],[20]],[None]],

                                "Bullet Seed":[["Gra"],[[20],[100],[30]],[None]],
                                "Solar Beam":[["Gra"],[[120],[100],[10]],[None]],
                                "Petal Dance":[["Gra"],[[120],[100],[10]],[None]],
                                "Stun Spore":[["Gra"],[[0],[75],[30]],["Para",1]],
                                "Poisonpowder":[["Gra"],[[0],[75],[35]],["Poison",1]],
                                "Mega Drain":[["Gra"],[[40],[100],[15]],[None]],
                                "Grass Knot":[["Gra"],[[60],[100],[20]],[None]],
                                "Leech Seed":[["Gra"],[[0],[90],[10]],[None]],
                                "Frenzy Plant":[["Gra"],[[150],[90],[6]],[None]],
                                "Absorb":[["Gra"],[[20],[100],[25]],[None]],
                                "Leaf Storm":[["Gra"],[[130],[90],[5]],[None]],
                                "Power Whip":[["Gra"],[[120],[85],[5]],[None]],
                                "Giga Drain":[["Gra"],[[75],[100],[10]],[None]],
                                "Needle Arm":[["Gra"],[[60],[100],[15]],["Flinch",3/10]],
                                "Seed Bomb":[["Gra"],[[80],[100],[15]],[None]],
                                "Leaf Blade":[["Gra"],[[90],[100],[15]],["HighCrit",1]],
                                "Vine Whip":[["Gra"],[[45],[100],[25]],[None]],
                                "Razor Leaf":[["Gra"],[[55],[95],[25]],["HighCrit",1]],
                                "Magical Leaf":[["Gra"],[[60],[100],[20]],[None]],
                                "Sleep Powder":[["Gra"],[[0],[75],[15]],["Sleep",1]],
                                "Leech Life":[["Gra"],[[20],[100],[15]],[None]],

                                "Magnitude":[["Gro"],[[60],[100],[30]],[None]],
                                "Mud Shot":[["Gro"],[[55],[95],[15]],[None]],
                                "Sand Attack":[["Gro"],[[0],[100],[15]],[None]],
                                "Sand Tomb":[["Gro"],[[60],[100],[20]],[None]],
                                "Bone Rush":[["Gro"],[[25],[90],[10]],[None]],
                                "Bone Club":[["Gro"],[[65],[85],[20]],["Flinch",1/10]],
                                "Bonemerang":[["Gro"],[[50],[90],[10]],[None]],
                                "Earthquake":[["Gro"],[[100],[100],[10]],[None]],
                                "Earth Power":[["Gro"],[[90],[100],[10]],[None]],
                                "Dig":[["Gro"],[[80],[100],[10]],[None]],
                                "Mud Bomb":[["Gro"],[[65],[85],[10]],[None]],
                                "Mud Slap":[["Gro"],[[20],[100],[10]],[None]],

                                "Ice Punch":[["Ice"],[[75],[100],[15]],["Freeze",1/10]],
                                "Avalanche":[["Ice"],[[60],[100],[10]],[None]],
                                "Ice Shard":[["Ice"],[[40],[100],[30]],[None]],
                                "Icicle Spear":[["Ice"],[[25],[100],[30]],[None]],
                                "Ice Fang":[["Ice"],[[65],[95],[15]],["Freeze",1/10]],
                                "Icy Wind":[["Ice"],[[55],[95],[15]],[None]],
                                "Powder Snow":[["Ice"],[[40],[100],[25]],["Freeze",1/10]],
                                "Blizzard":[["Ice"],[[110],[70],[5]],["Freeze",1/10]],
                                "Aurora Beam":[["Ice"],[[65],[100],[20]],[None]],
                                "Ice Beam":[["Ice"],[[90],[100],[10]],["Freeze",1/10]],

                                "Constrict":[["Nor"],[[10],[100],[35]],[None]],
                                "Slam":[["Nor"],[[80],[75],[20]],[None]],
                                "Explosion":[["Nor"],[[250],[100],[1]],[None]],
                                "Wrap":[["Nor"],[[15],[90],[20]],[None]],
                                "Razor Wind":[["Nor"],[[80],[100],[10]],["HighCrit",1]],
                                "Headbutt":[["Nor"],[[70],[100],[15]],[None]],
                                "Horn Drill":[["Nor"],[[0],[0],[5]],[None]],
                                "Bind":[["Nor"],[[15],[85],[20]],[None]],
                                "Growl":[["Nor"],[[0],[100],[40]],[None]],
                                "Facade":[["Nor"],[[70],[100],[20]],[None]],
                                "Sing":[["Nor"],[[0],[55],[15]],["Sleep",1]],
                                "Softboiled":[["Nor"],[[0],[0],[10]],[None]],
                                "Rage":[["Nor"],[[20],[100],[20]],[None]],
                                "Retaliation":[["Nor"],[[70],[100],[5]],[None]],
                                "Skull Bash":[["Nor"],[[130],[100],[10]],[None]],
                                "Last Resort":[["Nor"],[[140],[100],[5]],[None]],
                                "Egg Bomb":[["Nor"],[[100],[75],[10]],[None]],
                                "Leer":[["Nor"],[[0],[100],[30]],[None]],
                                "Fury Attack":[["Nor"],[[15],[85],[20]],[None]],
                                "Body Slam":[["Nor"],[[85],[100],[15]],["Para",3/10]],
                                "Crush Claw":[["Nor"],[[75],[95],[10]],[None]],
                                "Take Down":[["Nor"],[[90],[85],[20]],[None]],
                                "Double Slap":[["Nor"],[[15],[85],[10]],["Multi",1]],
                                "Double Hit":[["Nor"],[[35],[90],[10]],[None]],
                                "Secret Power":[["Nor"],[[70],[100],[20]],[None]],
                                "Fury Swipes":[["Nor"],[[18],[80],[15]],[None]],
                                "Slash":[["Nor"],[[70],[100],[20]],["HighCrit",1]],
                                "Swords Dance":[["Nor"],[[40],[10],[30]],[None]],
                                "Tackle":[["Nor"],[[50],[100],[35]],[None]],
                                "Extremespeed":[["Nor"],[[80],[100],[5]],[None]],
                                "Tail Whip":[["Nor"],[[0],[100],[30]],[None]],
                                "Pound":[["Nor"],[[120],[100],[15]],[None]],
                                "Double Edge":[["Nor"],[[40],[100],[30]],[None]],
                                "Rock Climb":[["Nor"],[[90],[85],[20]],["Confuse",1/5]],
                                "Dizzy Punch":[["Nor"],[[70],[100],[10]],["Confuse",1/5]],
                                "Hyper Beam":[["Nor"],[[150],[90],[5]],[None]],
                                "Screech":[["Nor"],[[0],[85],[40]],[None]],
                                "Scratch":[["Nor"],[[40],[100],[35]],[None]],
                                "Smokescreen":[["Nor"],[[0],[100],[20]],[None]],
                                "Giga Impact":[["Nor"],[[150],[90],[5]],[None]],
                                "False Swipe":[["Nor"],[[40],[100],[40]],[None]],
                                "Pay Day":[["Nor"],[[40],[100],[20]],[None]],
                                "Hyper Voice":[["Nor"],[[90],[100],[10]],[None]],
                                "Supersonic":[["Nor"],[[0],[55],[20]],["Confuse",1]],
                                "Guillotine":[["Nor"],[[0],[0],[5]],[None]],
                                "Mega Kick":[["Nor"],[[120],[75],[5]],[None]],
                                "Comet Punch":[["Nor"],[[90],[100],[10]],[None]],
                                "Swift":[["Nor"],[[60],[100],[20]],[None]],
                                "Lovely Kiss":[["Nor"],[[0],[75],[10]],["Sleep",1]],
                                "Mega Punch":[["Nor"],[[18],[85],[15]],[None]],
                                "Sonicboom":[["Nor"],[[0],[90],[20]],[None]],
                                "Rapid Spin":[["Nor"],[[20],[100],[40]],[None]],
                                "Rest":[["Nor"],[[0],[0],[10]],[None]],
                                "Yawn":[["Nor"],[[0],[0],[10]],[None]],
                                "Hyper Fang":[["Nor"],[[80],[90],[15]],[None]],
                                "Vicegrip":[["Nor"],[[55],[100],[30]],[None]],
                                "Sweet Kiss":[["Nor"],[[0],[75],[10]],["Confuse",1]],
                                "Spike Cannon":[["Nor"],[[20],[100],[15]],[None]],
                                "Horn Attack":[["Nor"],[[65],[100],[25]],[None]],
                                "Thrash":[["Nor"],[[120],[100],[10]],[None]],
                                "Cut":[["Nor"],[[50],[95],[30]],[None]],
                                "Harden":[["Nor"],[[0],[0],[30]],[None]],
                                "Super Fang":[["Nor"],[[0],[90],[10]],[None]],
                                "Quick Attack":[["Nor"],[[40],[100],[30]],[None]],

                                "Clear Smog":[["Poi"],[[50],[100],[15]],[None]],
                                "Poison Jab":[["Poi"],[[80],[100],[20]],["Poison",3/10]],
                                "Poison Tail":[["Poi"],[[50],[100],[25]],["Poison",1/10]],
                                "Sludge Bomb":[["Poi"],[[90],[100],[10]],["Poison",3/10]],
                                "Toxic":[["Poi"],[[0],[90],[10]],["Poison",1]],
                                "Acid":[["Poi"],[[40],[100],[30]],[None]],
                                "Poison Gas":[["Poi"],[[0],[90],[40]],["Poison",1]],
                                "Poison Sting":[["Poi"],[[15],[100],[35]],["Poison",3/10]],
                                "Smog":[["Poi"],[[30],[70],[20]],["Poison",2/5]],
                                "Sludge":[["Poi"],[[65],[100],[20]],["Poison",3/10]],
                                "Poison Fang":[["Poi"],[[50],[100],[15]],["Poison",3/10]],
                                "Gunk Shot":[["Poi"],[[120],[80],[5]],["Poison",3/10]],

                                "Calm Mind":[["Psy"],[[0],[0],[20]],[None]],
                                "Luster Purge":[["Psy"],[[70],[100],[5]],[None]],
                                "Teleport":[["Psy"],[[0],[0],[20]],[None]],
                                "Psywave":[["Psy"],[[0],[80],[15]],[None]],
                                "Psybeam":[["Psy"],[[65],[100],[20]],["Confuse",1/10]],
                                "Psychic":[["Psy"],[[90],[100],[10]],[None]],
                                "Zen Headbutt":[["Psy"],[[80],[90],[15]],[None]],
                                "Psycho Cut":[["Psy"],[[70],[100],[20]],["HighCrit",1]],
                                "Extrasensory":[["Psy"],[[80],[100],[20]],[None]],
                                "Confusion":[["Psy"],[[50],[100],[25]],["Confuse",1/10]],
                                "Hidden Power":[["Psy"],[[60],[100],[15]],[None]],
                                "Synchro Noise":[["Psy"],[[50],[100],[15]],[None]],
                                "Stomp":[["Psy"], [[65], [100], [20]], [None]],
                                "Low Kick":[["Psy"], [[60], [100], [20]], [None]],

                                "Rock Slide":[["Roc"],[[75],[90],[10]],[None]],
                                "Stone Edge":[["Roc"],[[100],[80],[5]],["HighCrit",1]],
                                "Rollout":[["Roc"],[[30],[90],[20]],[None]],
                                "Rock Blast":[["Roc"],[[25],[90],[10]],[None]],
                                "Ancient Power":[["Roc"],[[60],[100],[5]],[None]],
                                "Rock Wrecker":[["Roc"],[[150],[90],[5]],[None]],
                                "Head Smash":[["Roc"],[[150],[80],[5]],[None]],
                                "Rock Throw":[["Roc"],[[50],[90],[15]],[None]],
                                "Rock Tomb":[["Roc"],[[60],[95],[15]],[None]],

                                "Steel Wing":[["Roc"],[[70],[90],[25]],[None]],
                                "Meteor Mash":[["Roc"],[[90],[90],[10]],[None]],
                                "Metal Burst":[["Roc"],[[0],[100],[10]],[None]],
                                "Magnet Bomb":[["Roc"],[[60],[100],[20]],[None]],
                                "Iron Tail":[["Roc"],[[100],[75],[15]],[None]],
                                "Metal Claw":[["Roc"],[[50],[95],[35]],[None]],
                                "Mirror Shot":[["Roc"],[[65],[85],[10]],[None]],
                                "Iron Head":[["Roc"],[[80],[100],[15]],[None]],
                                "Flash Cannon":[["Roc"],[[50],[100],[10]],[None]],

                                "Surf":[["Wat"],[[90],[100],[15]],[None]],
                                "Splash":[["Wat"],[[0],[0],[40]],[None]],
                                "Aqua Jet":[["Wat"],[[40],[100],[20]],[None]],
                                "Crabhammer":[["Wat"],[[100],[90],[10]],["HighCrit",1]],
                                "Aqua Tail":[["Wat"],[[90],[90],[10]],[None]],
                                "Bubblebeam":[["Wat"],[[65],[100],[20]],[None]],
                                "Muddy Water":[["Wat"],[[90],[85],[10]],[None]],
                                "Brine":[["Wat"],[[65],[100],[10]],[None]],
                                "Water Pulse":[["Wat"],[[60],[100],[20]],["Confuse",1/5]],
                                "Waterfall":[["Wat"],[[80],[100],[15]],[None]],
                                "Water Gun":[["Wat"],[[40],[100],[25]],[None]],
                                "Bubble":[["Wat"],[[40],[100],[30]],[None]],
                                "Hydro Pump":[["Wat"],[[110],[80],[10]],[None]],
                                "Uproar":[["Nor"],[[90],[100],[10]],[None]],
}



def Burn(self, if_run, mod):
                if if_run:
                                self.hp-=self.maxhp//16
                                self.condition[inspect.stack()[0][3]][2]=1/2

def Freeze(self, if_run, mod):
                freezet=1
                if if_run:
                                self.condition[inspect.stack()[0][3]][2]=0
                                x=randint(1,5)
                                if freezec==freezet:
                                                if_run=false


def Para(self, if_run, mod):
                if if_run:
                                parac=randint(1,4)
                                if parac==1:
                                                self.condition[inspect.stack()[0][3]][2]=0
                                else:
                                                self.condition[inspect.stack()[0][3]][2]=1

def Sleep(self,if_run,mod):
                if if_run:
                                sleepc=randint(1,3)
                                self.condition[inspect.stack()[0][3]][2]=0
                                sleepc-=1
                                if sleepc==0:
                                                if_run=False


def Poison(self,if_run,mod):
                if if_run:
                                self.hp-=self.maxhp//8

def BadPoison(self,if_run,mod):
                if if_run:
                                self.hp-=self.maxhp//self.badpoisonc
                                self.badpoisonc+=1/16

def Flinch(self,if_run,mod):
                if if_run:
                                self.condition[inspect.stack()[0][3]][2]=0

def Confuse(self,if_run,mod):
                if if_run:
                                self.cFlag=True
                                confusec=randint(1,4)
                                confusec-=1
                                if confusec==0:
                                                self.cFlag=False
                                                if_run=False



def HighCrit(self,if_run,mod):
                if if_run:
                                self.CHlist=[1,1,1,2,2]
                if not if_run:
                                self.CHlist=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2]

def Damage(Level,BaseP,SpAtk,SpDef,r,STAB,Weakness,CH,mod1):
                DamageDealt=trunc(trunc(trunc(trunc(trunc(trunc((trunc(trunc(trunc(trunc((trunc(Level*2/5)+2)*BaseP)*SpAtk)/50)/SpDef)+2)*CH)*r)/100)*STAB)*Weakness)*mod1)
                return DamageDealt

def Catchchance(hpMax,hpCurrent,rate,ball,status):
        a =round(((3*hpMax-2*hpCurrent)*(rate*ball))/((3*hpMax)*status))
        return a

def ShakeComparison(CatchChance,chart):
        #Chart is the 2D list of Pokemon Catchrates
        comparison=0
        BComp = open(chart, "rb")
        file=(pickle.loads(BComp.read()))
        for i in range(len(file)):
                if file[i][0]==CatchChance:
                        comparison=file[i][1]

        instant=randint(0,60)
        counter=0
        shakeList=[]

        if comparison<=instant:                                    #Instantally catch pokemon if chances are right.
                return "Caught"

        else:
                for i in range(3):                                      #Performs 3 chances for pokemon to excape.
                        shakeList.append(randint(0,255))

                for i in range(len(shakeList)):
                        if shakeList[i]<comparison:
                                counter+=1
                if counter==3:
                        return ["Caught",3]
                else:
                        return ["Escaped",counter]

def CatchFormula(hpMax,hpCurrent,rate,ball,status,chart):
        a=Catchchance(hpMax,hpCurrent,rate,ball,status)
        return ShakeComparison(a,chart)






##StartUserPokeHP=UserPoke[0][-1][0]
##CurrUserPokeHP=StartUserPokeHP
##
##StartOppPokeHP=opp[0][-1][0]
##CurrOppPokeHP=StartOppPokeHP
##
##for i in range(0,len(UserPoke)):
##    print("Your Pokemon: \n",UserPoke[i][0][0]+",",CurrUserPokeHP,"/",StartUserPokeHP)
##
##for i in range(0,len(opp)):
##    print(opp[0][0][0],":",CurrOppPokeHP,"/",StartOppPokeHP)
##
##print("Your Attacks:\n")
##for i in range(4):
##    print(i+1,UserPoke[0][4][i])
##
##userattackchoice=input("Enter the attack# you want")
##userattack=(UserPoke[0][4][int(userattackchoice)-1])
##

_POKEMON_ID = 0
class Pokemon(object):
                def __init__(self, *args):
                                self.exp = -1
                                self.level = -1
                                self.tID = -1
                                self.SpAtk = -1
                                self.SpDef = -1
                                self.type1 = -1
                                self.type2 = -1
                                self.hp = -1
                                self.maxhp = -1
                                self.skill = []
                                self.image_front = None
                                self.image_back = None
                                self.name = ""
                                self.id = 0
                                self.badpoisonc=1/16
                                self.skillpp = [0, 0, 0, 0]
                                self._last_effect = "Missed"
                                if args: self.load(*args)

                def load(self, identifer, xp, name=None, changeid=None):
                                global _POKEMON_ID
                                if changeid is None:
                                        _POKEMON_ID += 1
                                        self.id = _POKEMON_ID
                                else:
                                        self.id = changeid
                                if xp//500 <= 0: xp = 500
                                self.exp = xp
                                self.level = self.exp//500
                                if self.level > 100: self.level = 100
                                self.tID = identifer
                                self.SpAtk = PokeStat[identifer][3][0]+(self.level/2)
                                self.SpDef = PokeStat[identifer][3][1]+(self.level/2)
                                self.type1 = PokeStat[identifer][1][0]
                                self.type2 = PokeStat[identifer][1][-1]
                                self.hp = self.level*4
                                self.maxhp = self.level*4
                                self.skill = PokeStat[identifer][4][:]
                                self.image_front = None
                                self.image_back = None
                                if name is None: self.name = self.getName()
                                self.condition={"Burn":[self, False, 1], "Freeze":[self,False,1], "Para":[self,False,1],
                                                                "Sleep":[self,False,1], "Poison":[self,False,1], "BadPoison":[self,False,1],
                                                                "Flinch":[self,False,1], "HighCrit":[self,False,1]}

                                self.mod1=1
                                self.badpoisonc=1/16
                                self.cFlag=False
                                self.CHlist=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2]
                                self.CH=choice(self.CHlist)
                                self.cChance=PokeStat[identifer][5][0]
                                self.skillpp = []
                                for i in range(4): self.skillpp.append(self.getSkillPP_ori(i))
                                if isinstance(self.getEvolve()[0], int) and self.getEvolve()[0] <= self.level:
                                                self.evolve()


                def getID(self):
                                return self.tID

                def getName(self):
                                return PokeStat[self.tID][0][0]

                def getHP(self):
                                return self.hp

                def getSkill(self, skillno):
                                return self.skill[skillno]

                def getSkills(self):
                                return self.skill

                def getSkillP(self,skillno):
                                return attack[self.getSkill(skillno)][1][0][0]

                def getSkillT(self,skillno):
                                return attack[self.getSkill(skillno)][0][0]

                def getSkillA(self,skillno):
                                return attack[self.getSkill(skillno)][1][1][0]

                def getSkillBonus(self,skillno):
                                if attack[self.getSkill(skillno)][-1][0] is None:
                                                return None
                                else:
                                                return attack[self.getSkill(skillno)][-1][0]

                def getSkillBonusChance(self, skillno):
                                try: return attack[self.getSkill(skillno)][-1][1]
                                except: return 0

                def getSkillPP_ori(self, skillno):
                                return attack[self.getSkill(skillno)][1][2][0]

                def getSkillPP(self, skillno):
                                return self.skillpp[skillno]

                def getEvolve(self):
                                if self.getID!=133:
                                                if PokeStat[self.getID()][-1][0]!="Final Stage of Evolution":
                                                                #Checks if Pokemon can Evolve

                                                                if PokeStat[self.getID()][-1][1]=="Water Stone":
                                                                                return ["Water Stone","Stone"]
                                                                if PokeStat[self.getID()][-1][1]=="Leaf Stone":
                                                                                return ["Leaf Stone","Stone"]
                                                                if PokeStat[self.getID()][-1][1]=="Fire Stone":
                                                                                return ["Fire Stone","Stone"]
                                                                if PokeStat[self.getID()][-1][1]=="Moon Stone":
                                                                                return ["Moon Stone","Stone"]
                                                                if PokeStat[self.getID()][-1][1]=="Thunder Stone":
                                                                                return ["Thunder Stone","Stone"]

                                                                #If pokemon needs stones to evolve, use as stone

                                                                if isinstance(PokeStat[self.getID()][-1][1], int):

                                                                                return [PokeStat[self.getID()][-1][1]]
                                                                #If pokemon only needs to be a level, then it can evolve right away
                                                return ["Final Stage of Evolution"]
                                elif self.getID==133:
                                                return ["Final Stage of Evolution"]

                def evolve(self, using=None):
                                #   Special Case Eevee with multi evolutions
                                if self.getName()=="Eevee":
                                        if using=="Water Stone":
                                                        self.tID=134
                                        elif using=="Thunder Stone":
                                                        self.tID=135
                                        elif using=="Fire Stone":
                                                        self.tID=136
                                        else:
                                                return self.tID
                                        self.load(self.tID, self.exp, changeid=self.id)
                                        return self.tID


                                if self.getEvolve()[-1]=="Final Stage of Evolution":
                                                return self.getEvolve()

                                if self.getEvolve()[-1]=="Stone":
                                                #Normal Pokemon
                                                if using == self.getEvolve()[0]:
                                                        self.tID+=1
                                                        self.load(self.tID, self.exp, changeid=self.id)
                                if isinstance(self.getEvolve()[-1],int):
                                                if self.level>=self.getEvolve()[-1]:
                                                                self.tID+=1
                                                                self.load(self.tID, self.exp, changeid=self.id)
                                return self.tID



                                # if isinstance(self.getEvolve()[-1],int):
                                #       if self.getEvolve()[-1]<self.level:
                                #               self.tID+=1
                                #               return self.tID

                def get_evolve_item(self):
                                return pokestat[getID()][-1][1]

                def attack(self, other, skillno):
                                                if not self.getSkillPP(skillno):
                                                        self._last_effect="No PP Left"
                                                        return 0
                                                else: self.skillpp[skillno] -= 1

                                                self.condition["Flinch"][0] = other

                                                if self.getSkillBonus(skillno) is not None:
                                                                conditionList=[Burn,Freeze,Para,Sleep,Poison,BadPoison,Flinch,Confuse]
                                                                condition=[]
                                                                for i in range (len(conditionList)):
                ##                              print(self.getSkillBonus(skillno))
                                                                                if conditionList[i]==eval(self.getSkillBonus(skillno)):
                                                                                                condition.append (conditionList[i].__name__)
                                                                chance=self.getSkillBonusChance(skillno)
                                                                chancecheck=randint(0,100)
                                                                if 100*chance>chancecheck and condition:
                                                                                if condition[0] == "Confuse":
                                                                                        other.cFlag = True
                                                                                else:
                                                                                        other.condition[condition[0]][1] = True
                                                _no_action = False
                                                for i in self.condition:
                                                                val = eval(i)(*self.condition[i])
                                                                if i == "Para" and val == 0:
                                                                                _no_action = True
                                                                elif i == "Flinch" and val == 0:
                                                                                _no_action = True
                                                if _no_action:
                                                        self._last_effect="No Action"
                                                        return 0
                                                self._last_effect="Missed"
                                                accCheckv=self.getSkillA(skillno)
                                                accCheck=randint(0,100)
                                                if accCheck<=accCheckv:
                                                                if self.cFlag and randint(0, 1):
                                                                            
                                                                                damage = Damage(self.level,
                                                                                                                self.getSkillP(skillno),
                                                                                                                self.SpAtk,
                                                                                                                self.SpDef,
                                                                                                                randint(85,100),
                                                                                                                STAB(self.type1,self.type2,self.getSkillT(skillno)),
                                                                                                                BonusCalc(self.getSkillT(skillno),self.type1,self.type2)[0],
                                                                                                                self.CH,self.mod1)
                                                                                if not self.getSkillP(skillno): damage = 0
                                                                                self._last_effect = BonusCalc(self.getSkillT(skillno),self.type1,self.type2)[1]
                                                                                self._last_effect+="\nAttacked your pokemon itself. Damage: %d"%damage
                                                                                self.hp-=damage
                                                                                damage = 0
                                                                else:
                                                                                damage = Damage(self.level,
                                                                                                                self.getSkillP(skillno),
                                                                                                                self.SpAtk,
                                                                                                                other.SpDef,
                                                                                                                randint(85,100),
                                                                                                                STAB(self.type1,self.type2,self.getSkillT(skillno)),
                                                                                                                BonusCalc(self.getSkillT(skillno),other.type1,other.type2)[0],
                                                                                                                self.CH,self.mod1)
                                                                                if not self.getSkillP(skillno): damage = 0
                                                                                self._last_effect = BonusCalc(self.getSkillT(skillno),other.type1,other.type2)[1]
                                                                                self._last_effect+="\nDamage: %d"%damage
                                                                other.hp -= damage
                                                                if other.hp < 0: other.hp = 0

                                                                return damage

                                                elif accCheck>=accCheckv:
                                                                return 0

                def get_str(self):
                                return self._last_effect

                def getProperties(self):
                                return {} # all properties

                def render(self, front=True):   # basic image -> no anim.
                                                if self.image_front is None:
                                                                                self.image_front = pygame.image.load(path+"/pokedex-media/pokemon/"
                                                                                                                                                                  "main-sprites/platinum/%d.png"%self.tID)\
                                                                                                                .convert_alpha()
                                                                                self.image_front = pygame.transform.scale(self.image_front, (200, 200))
                                                if self.image_back is None:
                                                                                self.image_back = pygame.image.load(path+"/pokedex-media/pokemon/"
                                                                                                                                                                 "main-sprites/platinum/back/%d.png"%
                                                                                                                                                                                                                                                                                                                                                                                self.tID)\
                                                                                                                .convert_alpha()
                                                                                self.image_back = pygame.transform.scale(self.image_back, (200, 200))
                                                if front: return self.image_front
                                                else: return self.image_back

                def get_size(self, front=True):
                                if front: return self.image_front.get_size()
                                else: return self.image_back.get_size()

                def get_hp_percentage(self):
                                return (self.hp/self.maxhp)*100

                def get_exp_percentage(self):
                                if self.exp >= 50000: return (self.exp-50000)/5
                                else: return (self.exp%500)/5

                def get_level(self):
                                return self.level

                def add_exp(self, exp):
                        self.exp += exp
                        level = self.exp//500
                        if level > 100: return
                        if level > self.level: self.load(self.tID, self.exp, self.name, changeid=self.id)

                def new(self):
                        p = self.__class__()
                        p.load(self.tID, self.exp)
                        return p



##print(userattack)s
##print((Damage((trunc(UserPoke[0][2][0]/500)),\
##             (attack[userattack][1][0][0]),\
##             (trunc(PokeStat[1][3][0]+(UserPoke[0][2][0]/500)*1/2)),\
##             (trunc(PokeStat[1][3][1]+(opp[0][3][0]/500)*1/2)),\
##             100,\
##             (STAB(PokeStat[1][3][0],PokeStat[1][3][1],attack[UserPoke[0][4][0]][0])),\
##             BonusCalc((attack[userattack][0][0]),opp[0][1][0],opp[0][1][-1]),\
##             1)))

# a = Pokemon()
# a.load(10, 2500)
# b = Pokemon()
# b.load(15, 4000)
# print(a.hp, b.hp)
# print(a.attack(b, 2))
# print(a.hp, b.hp)
# print(b.attack(a, 0))
# print(a.hp, b.hp)


class Character(g_object):
                def __init__(self,name,typ,level):
                                self._level=level
                                super(Character, self).__init__(typ, name)

class Player(Character):
                def __init__(self, pokemons, items, name, level, money, typ=TYPE_PLAYER):
                # def __init__(self, pokemons, name, level, money):
                                for i in items:
                                                if not issubclass(i.__class__, item): raise ValueError(type(items))
                                # global _CURRENT_ID
                                super(Player, self).__init__(name, typ, level)
                                # self.id = _CURRENT_ID
                                # _CURRENT_ID += 1
                                self.pokemon = []
                                self.backpack = {}
                                self.money = money
                                self.pokemon_save = []  # computer npc
                                # if not pokemons: raise ValueError(len(pokemons))    # at least one
                                for i in pokemons:
                                                self.pokemon.append(i)
                                for i in items:
                                                i.setOwner(self)
                                                self.backpack[i.id] = i
                                self.tasks = {}

                                self.info =  {"c_tme": int(time.time()),
                                                          "catch_record": {},   # tID: count, (last)time.time())
                                                          "accomplishment": [], # (name, time.time())
                                                          }
                                self.g_info = [-1, -1]

                def savePokemon(self, p_uniq_id):
                                if len(self.pokemon) == 1: return False
                                for i in self.pokemon:
                                        if i.id == p_uniq_id:
                                                self.pokemon_save.append(i)
                                                self.pokemon.remove(i)
                                                break
                                return True

                def loadPokemon(self, p_uniq_id):
                                if len(self.pokemon)+1 > 6: return False
                                for i in self.pokemon_save:
                                        if i.id == p_uniq_id:
                                                self.pokemon.append(i)
                                                self.pokemon_save.remove(i)
                                                break
                                return True

                def getCurrentPokemon(self):
                                return self.pokemon[0]

                def addPokemon(self, Pokemon_inst):
                                self.pokemon.append(Pokemon_inst)

                def delPokemon(self, p_uniq_id):
                                if self.getCurrentPokemon().id == p_uniq_id: raise ValueError("COULD NOT DEL CURRENT POKEMON")
                                for i in self.pokemon:
                                                if i.id == p_uniq_id:
                                                                self.pokemon.remove(i)

                def getNextAlivePokemon(self):
                                for i in self.pokemon:
                                                if i.getHP() > 0:
                                                                return i
                                return None

                def setCurrentPokemon(self, p_uniq_id):
                                if self.getCurrentPokemon().id != p_uniq_id:
                                                for i in range(len(self.pokemon)):
                                                                if self.pokemon[i].id == p_uniq_id:
                                                                                self.pokemon.insert(0, self.pokemon.pop(i))

                def evolve(self):
                                ids=[]
                                for i in self.backpack:
                                                if self.backpack[i].name==self.getCurrentPokemon().getEvolve()[0]:
                                                                ids.append(i)
                                for i in ids:
                                                self.useItem(i)
                                self.getCurrentPokemon().evolve()


                def addItem(self, item_inst):
                                if issubclass(item_inst.__class__, item):
                                                item_inst.setOwner(self)
                                                if item_inst.id in self.backpack:
                                                        self.backpack[item_inst.id].count += item_inst.count
                                                        return False, self.backpack[item_inst.id]
                                                for i in self.backpack:
                                                        if self.backpack[i].name == item_inst.name:
                                                                self.backpack[i].count += item_inst.count
                                                                return False, self.backpack[i]
                                                self.backpack[item_inst.id] = item_inst
                                                return True, self.backpack[item_inst.id]
                                else: raise ValueError(type(item_inst))

                def delItem(self, item_id):
                                if item_id in self.backpack:
                                                del self.backpack[item_id]

                def useItem(self, item_id, other=None):
                                if item_id in self.backpack:
                                                r = self.backpack[item_id].use(other)
                                                if self.backpack[item_id].count <= 0:
                                                                del self.backpack[item_id]
                                                return r
                                raise ValueError(item_id)

                def getItem(self, item_id):
                                if item_id in self.backpack:
                                                return self.backpack[item_id]
                                return None

                def getBackpackInfo(self):
                                li = list(map((lambda x: x.getInfo()), self.backpack.values()))
                                li.sort()
                                return li

                def check_backpack(self):
                                lidel = []
                                for i in self.backpack:
                                                if self.backpack[i].count <= 0:
                                                                lidel.append(i)
                                for i in lidel:
                                        del self.backpack[i]

                def open_task(self, identifier, *init_args):
                                if identifier in self.tasks:
                                                return False, self.tasks[identifier]
                                else:
                                                self.tasks[identifier] = Task(*init_args)
                                                return True, self.open_task(identifier)[1]

                def del_task(self, identifier):
                                if identifier in self.tasks: del self.tasks[identifier]

                def check_prev_task(self, prev):
                                for i in prev:
                                                if i not in self.tasks: return False
                                                if not self.tasks[i].done: return False
                                return True

                def save(self):
                        for i in self.pokemon:
                                i.image_front = None
                                i.image_back = None
                        self._res = None
                        self.g_info = [_POKEMON_ID, _ITEM_ID]

                def load(self):
                        global _POKEMON_ID, _ITEM_ID
                        if self.g_info != [-1, -1]:
                                _POKEMON_ID = self.g_info[0]
                                _ITEM_ID = self.g_info[1]
                        import ChiangObjectives as co
                        self._res = co._res[self._name]



class Task(object):
        def __init__(self, prev=[], name="Task"):
                self.stage = 0
                self.prev = prev
                self.done = False
                self.name = name



_ITEM_ID = 0
class item(object):
                def __init__(self, name, count=1, buy_price=0, sell_price=0, owner=None):
                                global _ITEM_ID

                                _ITEM_ID += 1
                                self.id = _ITEM_ID

                                self.name = name
                                self.owner = owner
                                self.count = count
                                self.buy_price = buy_price
                                self.sell_price = sell_price

                def setOwner(self, owner):
                                self.owner = owner

                def getInfo(self):
                                return self.name, self.id

                def getType(self):
                                return items[self.name][-1][0]

                def use(self, other):
                                if self.count <= 0: raise ValueError(self.count)
                                result = self.apply(other)
                                if result is not None: self.count -= 1
                                return result

                def apply(self, other):
                        pass
                                # self.owner apply item
                                # return if successfully applied

                def describe(self):
                        return "description here"

                def sell(self, count):
                                if count > self.count: raise ValueError(count)
                                self.count -= count
                                self.owner.money += count * self.sell_price

                def buy(self, count):
                                if count < 0: raise ValueError(count)
                                if count*self.buy_price <= self.owner.money:
                                        self.owner.money -= count*self.buy_price
                                        self.count += count
                                else: raise ValueError(self.owner.money)

                def getMaxBuy(self):
                                return self.owner.money//self.buy_price

                def getMaxSell(self):
                                return self.count

items={"Pokeball":[[1],[200],["A device for catching wild Pokémon.It's thrown like a ball at a Pokémon, comfortably encapsulating its target."],["Pokeball"]],
           "Great Ball":[[1.5],[600],["A good, high-performance Poké Ball that provides a higher Pokémon catch rate than a standard Poké Ball can."],["Pokeball"]],
           "Ultra Ball":[[2],[1200],["An ultra-high performance Poké Ball that provides a higher success rate for catching Pokémon than a Great Ball."],["Pokeball"]],
           "Master Ball":[[255],[20000],["The best Poké Ball with the ultimate level of performance. With it, you will catch any wild Pokémon without fail."],["Pokeball"]],
           "Potion":[[20],[300],["A spray-type medicine for treating wounds. It can be used to restore 20 HP to an injured Pokémon."],["Potion"]],
           "Super Potion":[[50],[700],["A spray-type medicine for treating wounds. It can be used to restore 50 HP to an injured Pokémon."],["Potion"]],
           "Hyper Potion":[[200],[1200],["A spray-type medicine for treating wounds.It can be used to restore 200 HP to an injured Pokémon."],["Potion"]],
           "Max Potion":[[9999],[2500],["A spray-type medicine for treating wounds. It will completely restore the max HP of a single Pokémon."],["Potion"]],
           "Full Restore":[[9999],[2500],["A medicine that can be used to fully restore the HP of a single Pokémon and heal any status conditions it has."],["Potion"]],
           "Antidote":[["Poison","BadPoison"],[100],["A spray-type medicine for poisoning. It can be used once to lift the effects of being poisoned from a Pokémon."],["Potion"]],
           "Parlyz Heal":[["Para"],[200],["A spray-type medicine for paralysis. It can be used once to free a Pokémon that has been paralyzed."],["Potion"]],
           "Awakening":[["Sleep"],[250],["A spray-type medicine used against sleep. It can be used once to rouse a Pokémon from the clutches of sleep."],["Potion"]],
           "Burn Heal":[["Burn"],[250],["A spray-type medicine for treating burns. It can be used once to heal a Pokemon suffering from a burn."],["Potion"]],
           "Ice Heal":[["Freeze"],[100],["A spray-type medicine for freezing. It can be used once to defrost a Pokémon that has been frozen solid."],["Potion"]],
           "Fire Stone":[[1200],["A peculiar stone that can make certain species of Pokémon evolve. The stone has a fiery orange heart."], ["Stone"]],
           "Thunder Stone":[[1200],["A peculiar stone that can make certain species of Pokémon evolve. It has a distinct thunderbolt pattern."],["Stone"]],
           "Water Stone":[[1200],["A peculiar stone that can make certain species of Pokémon evolve. It is the blue of a pool of clear water."],["Stone"]],
           "Leaf Stone":[[1200],["A peculiar stone that can make certain species of Pokémon evolve. It has an unmistakable leaf pattern."],["Stone"]],
           "Moon Stone":[[1200],["A peculiar stone that can make certain species of Pokémon evolve. It is as black as the night sky."],["Stone"]],}




ITEM_NOTUSED = None
ITEM_USED = 0
ITEM_CAUGHT = 1
class Item(item):
                def describe(self):
                        return items[self.name][-2][0]

                def apply(self, other):
                                pkmon = self.owner.getCurrentPokemon()
                                if other is not None: otherpkmon=other.getCurrentPokemon()
                                else: otherpkmon = None

                                if self.getType()=="Stone":
                                                if self.name==pkmon.getEvolve()[0]:
                                                        pkmon.evolve(self.name)
                                                        return ITEM_USED

                                elif self.getType()=="Potion":
                                                if self.name=="Potion":
                                                                pkmon.hp+= item(items[self.name][0])
                                                                if pkmon.hp+item(items[self.name][0])>pkmon.maxhp:
                                                                                pkmon.hp=pkmon.maxhp

                                                elif self.name=="Super Potion":
                                                                pkmon.hp+= item(items[self.name][0])
                                                                if pkmon.hp+item(items[self.name][0])>pkmon.maxhp:
                                                                                pkmon.hp=pkmon.maxhp

                                                elif self.name=="Hyper Potion":
                                                                pkmon.hp+= item(items[self.name][0])
                                                                if pkmon.hp+item(items[self.name][0])>pkmon.maxhp:
                                                                                pkmon.hp=pkmon.maxhp

                                                elif self.name=="Max Potion":
                                                                pkmon.hp=pkmon.maxhp


                                                elif self.name=="Antidote":
                                                                if pkmon.condition["Poison"][1]is True:
                                                                                pkmon.condition["Poison"][1]= False

                                                elif self.name=="Parlyz Heal":
                                                                if pkmon.condition["Para"][1]is True:
                                                                                pkmon.condition["Para"][1]= False

                                                elif self.name=="Parlyz Heal":
                                                                if pkmon.condition["Para"][1]is True:
                                                                                pkmon.condition["Para"][1]= False

                                                elif self.name=="Awakening":
                                                                if pkmon.condition["Sleep"][1]is True:
                                                                                pkmon.condition["Sleep"][1]= False

                                                elif self.name=="Burn Heal":
                                                                if pkmon.condition["Burn"][1]is True:
                                                                                pkmon.condition["Burn"][1]= False

                                                elif self.name=="Ice Heal":
                                                                if pkmon.condition["Freeze"][1]is True:
                                                                                pkmon.condition["Freeze"][1]= False

                                                return ITEM_USED

                                elif self.getType()=="Pokeball" and other is not None and other.getType() == TYPE_WILD:
                                                # self.owner.pokemon.append(otherpkmon)
                                                # return ITEM_CAUGHT
                                                if len(self.owner.pokemon) >= 6:
                                                        return
                                                if self.name=="Pokeball":
                                                            
                                                                x=CatchFormula(otherpkmon.maxhp,otherpkmon.hp,otherpkmon.cChance,1,1,"BComparison2.txt")
                                                                if x[0]=="Caught":
                                                                                self.owner.pokemon.append(otherpkmon)
                                                                                if otherpkmon.tID in self.owner.info["catch_record"]:
                                                                                        count, last_tme = self.owner.info["catch_record"][otherpkmon.tID]
                                                                                        self.owner.info["catch_record"][otherpkmon.tID] = count+1, time.time()
                                                                                else:
                                                                                        self.owner.info["catch_record"][otherpkmon.tID] = 1, time.time()
                                                                                return ITEM_CAUGHT


                                                                elif x[0]=="Escaped":
                                                                                pass

                                                elif self.name=="Great Ball":
                                                                x=CatchFormula(otherpkmon.maxhp,otherpkmon.hp,otherpkmon.cChance,1.5,1,"BComparison2.txt")
                                                                if x[0]=="Caught":
                                                                                self.owner.pokemon.append(otherpkmon)
                                                                                if otherpkmon.tID in self.owner.info["catch_record"]:
                                                                                        count, last_tme = self.owner.info["catch_record"][otherpkmon.tID]
                                                                                        self.owner.info["catch_record"][otherpkmon.tID] = count+1, time.time()
                                                                                else:
                                                                                        self.owner.info["catch_record"][otherpkmon.tID] = 1, time.time()
                                                                                return ITEM_CAUGHT


                                                                elif x[0]=="Escaped":
                                                                                pass
                                                elif self.name=="Ultra Ball":
                                                                x=CatchFormula (otherpkmon.maxhp,otherpkmon.hp,otherpkmon.cChance,2,1,"BComparison2.txt")
                                                                if x[0]=="Caught":
                                                                                self.owner.pokemon.append(otherpkmon)
                                                                                if otherpkmon.tID in self.owner.info["catch_record"]:
                                                                                        count, last_tme = self.owner.info["catch_record"][otherpkmon.tID]
                                                                                        self.owner.info["catch_record"][otherpkmon.tID] = count+1, time.time()
                                                                                else:
                                                                                        self.owner.info["catch_record"][otherpkmon.tID] = 1, time.time()
                                                                                return ITEM_CAUGHT


                                                                elif x=="Escaped":
                                                                                pass



                                                elif self.name=="Master Ball" and other is not None and other.getType() == TYPE_WILD:
                                                                x=CatchFormula(otherpkmon.maxhp,otherpkmon.hp,otherpkmon.cChance,255,1,"BComparison2.txt")
                                                                if x[0]=="Caught":
                                                                                self.owner.pokemon.append(otherpkmon)
                                                                                if otherpkmon.tID in self.owner.info["catch_record"]:
                                                                                        count, last_tme = self.owner.info["catch_record"][otherpkmon.tID]
                                                                                        self.owner.info["catch_record"][otherpkmon.tID] = count+1, time.time()
                                                                                else:
                                                                                        self.owner.info["catch_record"][otherpkmon.tID] = 1, time.time()
                                                                                return ITEM_CAUGHT


                                                                elif x[0]=="Escaped":
                                                                                pass

                                                return ITEM_USED

                                return ITEM_NOTUSED

gLeader={
        1:[["Brock"],[Pokemon(74,13*500),Pokemon(95,15*500)],["Boulder_Badge"]],
        2:[["Misty"],[Pokemon(120,20*500),Pokemon(121,22*500)],["Cascade_Badge"]],
        3:[["Lt. Surge"],[Pokemon(25,28*500),Pokemon(29,31*500),Pokemon(26,31*500)],["Thunder_Badge"]],
        4:[["Erika"],[Pokemon(71,35*500),Pokemon(114,34*500),Pokemon(45,36*500)],["Rainbow_Badge"]],
        5:[["Sabrina"],[Pokemon(64,39*500),Pokemon(122,42*500),Pokemon(49,40*500)],["Marsh_Badge"]],
        6:[["Koga"],[Pokemon(109,48*500),Pokemon(89,50*500),Pokemon(110,55*500)],["Soul_Badge"]],
        7:[["Blaine"],[Pokemon(58,58*500),Pokemon(77,57*500),Pokemon(78,60*500),Pokemon(126,61*500),Pokemon(59,64*500)],["Volcano_Badge"]],
        8:[["Giovanni"],[Pokemon(111,69*500),Pokemon(112,72*500),Pokemon(51,70*500),Pokemon(31,78*500),Pokemon(34,78*500),Pokemon(112,80*500)],["Earth_Badge"]]
        }



player=Player([],[Item("Pokeball", 5, 1000, 100)],"name", 0, 11000)


# for i in player.backpack:
#               if player.backpack[i].name == "Master Ball":
#                               result = i
#                               break
# print(player.useItem(result, other))
# print(player.pokemon)

