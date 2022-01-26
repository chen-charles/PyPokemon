import rgine.loader, rgine.exception
loader = rgine.loader.Loader("Initializing Game ... ", "__pokemon_game_loader")
loader.init()

try:
        import pickle
        import pygame
        import os
        import inspect
        os.chdir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        
        import rgine
        import base as base
        import menu as menu
        import battle as battle
        import backpack as backpack
        import Combinedv2 as libpkmon
        import map as maps

        textureSize = 32
        ScreenSize = list(map(int, (16*textureSize*1.5, 9*textureSize*1.5)))

        screen = pygame.display.set_mode(ScreenSize)
        pygame.display.set_icon(pygame.transform.scale(pygame.image.load(os.path.join("resources", "Launch.ico")), (32, 32)).convert_alpha())
        pygame.display.set_caption("Pokemon", "Pokemon")
        bkg = pygame.image.load(os.path.join("resources","Background.png")).convert_alpha()
        intro_imgs = []
        for root, dirs, files in os.walk(os.path.join("resources", "intro")):
                for i in files: intro_imgs.append(os.path.join(root, i))
        intro_imgs.sort()
        for i in range(len(intro_imgs)):
                intro_imgs[i] = pygame.image.load(intro_imgs[i]).convert_alpha()

        def LoadMap(uPos):
                global g_cm, world, terrain
                g_cm = mapManager.setMap(uPos)
                world = g_cm.world
                terrain = g_cm.terrain
                surf = g_cm.getBattleBk()
                if surf is not None: uBattle.setBackground(surf)

        def LoadPlayer(player, resetPos=False, battleStepCount=[2, 20]):
                global npcManager, pEventList, runningNpcEvent, pManager, uMe, uMenu, uBackpack, uBattle, uPokedex
                npcManager = base.NPCManager()
                for i in base.npcs:
                        base.npcs[i].setPlayer(player)
                        base.npcs[i].setPos(i)
                        npcManager.new(i[0], i[1], base.npcs[i])

                pEventList = []
                runningNpcEvent = base.NPC(None, None)


                pManager = base.PlayerManager(player, terrain, base.playerEvent, npcManager)
                if resetPos: pManager.getPlayer().setPos(212, 122)

                menu.inst[1].setPlayer(pManager.getPlayer())
                uMe = menu.inst[1]
                uPokedex = menu.inst[5]
                uMenu = menu.init_menu(menu.buttons, menu.inst)
                uBackpack = backpack.Backpack(wm, pManager.getPlayer())
                uBattle = battle.Battle(uBackpack, wm)
                menu.inst[2].setBackpack(uBackpack)
                uPokedex.setPlayer(pManager.getPlayer())

                LoadMap(pManager.getPlayer().getPos())

                pManager.setBattleStepCount(battleStepCount)

                setBattle(uBattleNPCs)

        base.npcs[(6, 3)].LoadMap = LoadMap
        base.npcs[(1, 300)].LoadMap = LoadMap
        def Release():
                global pEventList
                pManager.release()
                for i in pEventList: i.release(wm)
                pEventList = []
                if runningNpcEvent.isRunning(): runningNpcEvent.release(wm)
                uMenu.release(wm)
                uBattle.release(wm)
                wm.Release()
                pygame.quit()


        evt = rgine.Event()
        wm = rgine.windows.WindowsManager(ScreenSize)

        maps.init(ScreenSize, textureSize, os.path.join("BattleBackground"))
        mapManager = maps.MapManager()
        for i in base.maps:
                mapManager.add(maps.Map(*i))

        # terrain = base.init_terrain("Villiage1.terrain", "myTexture.texture", True, textureSize)
        # terrain.readTextureFromSurface(pygame.image.load("Villiage1.jpeg"))
        # terrain.readTerrainProperty("Villiage1.terrainProperty")
        # mapManager.add(maps.Map(terrain, (0, 0)))

        # uPos: [direction, newPos]
        # Map Id Starts From 0
        # Map Pos Formula: ((mapid%3-1)*100, (mapid-1)//3*100)
        # Example: mapid = 8 -> x: 100, 200

        def getMapOffset(mapid): return mapid%3*100, mapid//3*100
        def linkside(mapid, direction, bothway, sidelen=30):
                tx, ty = getMapOffset(mapid)
                if direction == pygame.K_LEFT:
                        for i in range(sidelen): mapManager.addLink((mx, my+i), direction, (tx+sidelen-1, ty+i), bothway)
                elif direction == pygame.K_RIGHT:
                        for i in range(sidelen): mapManager.addLink((mx+sidelen-1, my+i), direction, (tx, ty+i), bothway)
                elif direction == pygame.K_UP:
                        for i in range(sidelen): mapManager.addLink((mx+i, my), direction, (tx+i, ty+sidelen-1), bothway)
                elif direction == pygame.K_DOWN:
                        for i in range(sidelen): mapManager.addLink((mx+i, my+sidelen-1), direction, (tx+i, ty), bothway)
                else:
                        raise ValueError(direction)

        terrain = base.init_terrain(os.path.join("maps", "Map1", "1402438776.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map1", "1402438776.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map1", "1402965027.terrainProperty"))
        mx, my = getMapOffset(0)
        mapManager.add(maps.Map(terrain, (mx, my),typ=maps.MAP_TYPE_GRASS))
        linkside(1, pygame.K_RIGHT, True, 30)
        linkside(3, pygame.K_DOWN, True, 30)

        terrain = base.init_terrain(os.path.join("maps", "Map2", "1402359981.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map2", "1402359981.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map2", "1402601113.terrainProperty"))
        mx, my = getMapOffset(1)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))
        linkside(2, pygame.K_RIGHT, True, 30)

        terrain = base.init_terrain(os.path.join("maps", "Map3", "1402437430.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map3", "1402437430.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map3", "1402601167.terrainProperty"))
        mx, my = getMapOffset(2)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))
        linkside(5, pygame.K_DOWN, True, 30)
        mx, my = getMapOffset(13)
        mapManager.addLink((222, 9), pygame.K_UP, (mx+4, my+2), False)
        mapManager.addLink((mx+4, my+2), pygame.K_UP, (222, 9), False)


        terrain = base.init_terrain(os.path.join("maps", "Map4", "1402436018.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map4", "1402436018.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map4", "1402444571.terrainProperty"))
        mx, my = getMapOffset(3)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))
        linkside(4, pygame.K_RIGHT, True, 30)
        linkside(6, pygame.K_DOWN, True, 30)

        terrain = base.init_terrain(os.path.join("maps", "Map5", "1402432155.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map5", "1402432155.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map5", "1402964892.terrainProperty"))
        mx, my = getMapOffset(4)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))
        linkside(5, pygame.K_RIGHT, True, 30)

        terrain = base.init_terrain(os.path.join("maps", "Map6", "1402440441.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map6", "1402440441.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map6", "1402444027.terrainProperty"))
        mx, my = getMapOffset(5)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))
        linkside(8, pygame.K_DOWN, True, 30)
        tx, ty = getMapOffset(17)
        mapManager.addLink((mx+5, my+8), pygame.K_UP, (tx+3, ty+19), True)
        mapManager.addLink((tx+4, ty+19), pygame.K_DOWN, (mx+5, my+8), False)
        tx, ty = getMapOffset(19)
        mapManager.addLink((mx+8, my+22), pygame.K_UP, (tx+7, ty+9), True)
        tx, ty = getMapOffset(20)
        mapManager.addLink((mx+17, my+22), pygame.K_UP, (tx+3, ty+9), True)
        mapManager.addLink((tx+4, ty+9), pygame.K_DOWN, (mx+17, my+22), False)

        terrain = base.init_terrain(os.path.join("maps", "Map7", "1402442783.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map7", "1402442783.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map7", "1402754877.terrainProperty"))
        mx, my = getMapOffset(6)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))
        linkside(7, pygame.K_RIGHT, True, 30)
        tx, ty = getMapOffset(11)
        mapManager.addLink((mx+12, my+19), pygame.K_UP, (tx+5, ty+2), False)
        mapManager.addLink((tx+5, ty+2), pygame.K_UP, (mx+12, my+19), False)

        terrain = base.init_terrain(os.path.join("maps", "Map8", "1402449580.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map8", "1402449580.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map8", "1402754995.terrainProperty"))
        mx, my = getMapOffset(7)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))
        linkside(8, pygame.K_RIGHT, True, 30)

        terrain = base.init_terrain(os.path.join("maps", "Map9", "1402450816.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map9", "1402450816.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map9", "1402755120.terrainProperty"))
        mx, my = getMapOffset(8)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))

        terrain = base.init_terrain(os.path.join("maps", "Map10", "1402365834.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map10", "1402365834.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map10", "1402411654.terrainProperty"))
        mx, my = getMapOffset(9)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_ICE))
        tx, ty = getMapOffset(15)
        mapManager.addLink((mx+12, my+5), pygame.K_UP, (tx+7, ty+9), True)
        tx, ty = getMapOffset(16)
        mapManager.addLink((mx+19, my+5), pygame.K_UP, (tx+3, ty+9), True)
        mapManager.addLink((tx+4, ty+9), pygame.K_DOWN, (mx+19, my+5), False)
        tx, ty = getMapOffset(10)
        for i in range(30): mapManager.addLink((mx+i, my+29), pygame.K_DOWN, (tx+i, ty), True)

        terrain = base.init_terrain(os.path.join("maps", "Map11", "1402366964.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map11", "1402366964.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map11", "1402413654.terrainProperty"))
        mx, my = getMapOffset(10)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_GRASS))

        terrain = base.init_terrain(os.path.join("maps", "Map12", "1402490188.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map12", "1402490188.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map12", "1402755206.terrainProperty"))
        mx, my = getMapOffset(11)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_ROCK))
        tx, ty = getMapOffset(12)
        for i in range(30): mapManager.addLink((mx+i, my+29), pygame.K_DOWN, (tx+i, ty), True)

        terrain = base.init_terrain(os.path.join("maps", "Map13", "1402455174.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map13", "1402455174.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map13", "1402755242.terrainProperty"))
        mx, my = getMapOffset(12)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_ROCK))

        terrain = base.init_terrain(os.path.join("maps", "Map14", "1402522569.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map14", "1402522569.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map14", "1402881349.terrainProperty"))
        mx, my = getMapOffset(13)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_FIRE))
        tx, ty = getMapOffset(14)
        for i in range(30): mapManager.addLink((mx+i, my+29), pygame.K_DOWN, (tx+i, ty), True)

        terrain = base.init_terrain(os.path.join("maps", "Map15", "1402523290.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map15", "1402523290.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map15", "1402755322.terrainProperty"))
        mx, my = getMapOffset(14)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_FIRE))

        terrain = base.init_terrain(os.path.join("maps", "Map16", "1402626657.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map16", "1402626657.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map16", "1402627994.terrainProperty"))
        mx, my = getMapOffset(15)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_NONE))

        terrain = base.init_terrain(os.path.join("maps", "Map17", "1402629366.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map17", "1402629366.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map17", "1402629423.terrainProperty"))
        mx, my = getMapOffset(16)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_NONE))

        terrain = base.init_terrain(os.path.join("maps", "Map18", "1402631161.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map18", "1402631161.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map18", "1402755392.terrainProperty"))
        mx, my = getMapOffset(17)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_ELECTRIC))
        tx, ty = getMapOffset(18)
        for i in range(20): mapManager.addLink((mx+19, my+i), pygame.K_RIGHT, (tx, ty+i), True)

        terrain = base.init_terrain(os.path.join("maps", "Map19", "1402631505.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map19", "1402631505.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map19", "1402633094.terrainProperty"))
        mx, my = getMapOffset(18)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_ELECTRIC))

        terrain = base.init_terrain(os.path.join("maps", "Map16", "1402626657.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map16", "1402626657.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map16", "1402627994.terrainProperty"))
        mx, my = getMapOffset(19)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_NONE))

        terrain = base.init_terrain(os.path.join("maps", "Map17", "1402629366.terrain"), "myTexture.texture", True, textureSize)
        terrain.readTextureFromSurface(pygame.image.load(os.path.join("maps", "Map17", "1402629366.jpeg")))
        terrain.readTerrainProperty(os.path.join("maps", "Map17", "1402629423.terrainProperty"))
        mx, my = getMapOffset(20)
        mapManager.add(maps.Map(terrain, (mx, my), typ=maps.MAP_TYPE_NONE))

        uBattleNPCs = []
        for i in base.npcs:
                if "setBattle" in dir(base.npcs[i]):
                        uBattleNPCs.append(i)

        def setBattle(li):
                for i in li: npcManager.npcs[i].setBattle(uBattle)


        LoadPlayer(libpkmon.player, True)

        # Intro
        wmacros = rgine.windows.WindowsMacros()
        start = wm.CreateWindow(wmacros.WC_BUTTON, ((158//2, 59//2), wmacros.button, "Start"))
        wm.MoveWindow(start, 100, 100)
        load = wm.CreateWindow(wmacros.WC_BUTTON, ((158//2, 59//2), wmacros.button, "Load"))
        wm.MoveWindow(load, 100, 200)
        ext = wm.CreateWindow(wmacros.WC_BUTTON, ((158//2, 59//2), wmacros.button, "Exit"))
        wm.MoveWindow(ext, 100, 300)
        wm.SetTopmost(start, False)

        loader.release()
        result = 0
        while True:
                evt.update()
                if evt.type == pygame.QUIT:
                        Release()
                        exit(0)
                screen.fill((0, 0, 0))
                screen.blit(bkg, (0, 0))
                if evt.isKeyHit(pygame.K_UP):
                        if wm.GetTopmost() == ext: wm.SetTopmost(load, False)
                        elif wm.GetTopmost() == load: wm.SetTopmost(start, False)
                elif evt.isKeyHit(pygame.K_DOWN):
                        if wm.GetTopmost() == start: wm.SetTopmost(load, False)
                        elif wm.GetTopmost() == load: wm.SetTopmost(ext, False)
                for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
                        screen.blit(surface, pos)
                        if hWnd == start and msg == wmacros.HIT:
                                result = start
                        elif hWnd == load and msg == wmacros.HIT:
                                import wapisp
                                hPygameWindow = pygame.display.get_wm_info()["window"]
                                result, fname = wapisp.GetOpenFileName(hPygameWindow)
                                if result:
                                        try:
                                                with open(fname, "rb") as f:
                                                        player = pickle.load(f)
                                                player.load()
                                                LoadPlayer(player)
                                                result = load
                                        except:
                                                # if failed, exit (because the data loaded into player might be messy)
                                                hWnd = ext
                                else:
                                        pass

                        if hWnd == ext and msg == wmacros.HIT:
                                # Release
                                pManager.release()

                                for i in pEventList: i.release(wm)
                                pEventList = []

                                if runningNpcEvent.isRunning(): runningNpcEvent.release(wm)

                                uMenu.release(wm)
                                uBattle.release(wm)

                                wm.Release()

                                pygame.quit()
                                exit(1)

                pygame.display.flip()
                if result: break

        # Calling release to all present windows
        for i in wm: wm.DestroyWindow(i)

        if result == start:
                inpc = base.npcs[(-5, -5)]
                inpc.init(evt, wm)

                while True:
                        if wm.isWindowPresent(inpc.dbox):
                                evt.update()
                                if evt.type == pygame.QUIT:
                                        Release()
                                        exit(0)
                                wm.SetTopmost(inpc.dbox, False)
                                screen.fill((0, 0, 0))
                                surf, pos = inpc.render(evt, wm)
                                for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
                                        screen.blit(surface, pos)
                                pygame.display.flip()
                        else:
                                for i in wm: wm.DestroyWindow(i)
                                count = 0
                                while True:
                                        if count >= len(intro_imgs): break
                                        evt.update()
                                        screen.fill((0, 0, 0))
                                        screen.blit(intro_imgs[count], (0, 0))
                                        if evt.type == pygame.QUIT:
                                                Release()
                                                exit(0)
                                        if evt.isKeyHit(pygame.K_ESCAPE):
                                                break
                                        elif evt.isKeyHit(pygame.K_RETURN):
                                                count += 1
                                        pygame.display.flip()
                                sele1 = wm.CreateWindow(wmacros.WC_BUTTON,
                                                ((ScreenSize[0]//3, ScreenSize[1]), wmacros.button, "Bulbasaur")
                                )
                                sele1pic = pygame.transform.scale(pygame.image.load((os.path.join("pokedex-media","pokemon", "sugimori",
                                                                                                  "1.png"))), (260, 240)).convert_alpha()
                                sele2 = wm.CreateWindow(wmacros.WC_BUTTON,
                                                ((ScreenSize[0]//3, ScreenSize[1]), wmacros.button, "Charmander")
                                )
                                sele2pic = pygame.transform.scale(pygame.image.load((os.path.join("pokedex-media","pokemon", "sugimori",
                                                                                                  "4.png"))), (260, 240)).convert_alpha()
                                wm.MoveWindow(sele2, ScreenSize[0]//3, 0)
                                sele3 = wm.CreateWindow(wmacros.WC_BUTTON,
                                                ((ScreenSize[0]//3, ScreenSize[1]), wmacros.button, "Squirtle")
                                )
                                sele3pic = pygame.transform.scale(pygame.image.load((os.path.join("pokedex-media","pokemon", "sugimori",
                                                                                                  "7.png"))), (260, 240)).convert_alpha()
                                wm.MoveWindow(sele3, ScreenSize[0]//3*2, 0)
                                wm.SetTopmost(-1, False)
                                while True:
                                        evt.update()
                                        if evt.type == pygame.QUIT:
                                                Release()
                                                exit(0)
                                        screen.fill((0, 0, 0))
                                        screen.blit(sele1pic, (0, (ScreenSize[1]-sele1pic.get_height())//2))
                                        screen.blit(sele2pic, (260, (ScreenSize[1]-sele1pic.get_height())//2))
                                        screen.blit(sele3pic, (520, (ScreenSize[1]-sele1pic.get_height())//2))
                                        done = False
                                        for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
                                                screen.blit(surface, pos)
                                                if hWnd == sele1 and msg == wmacros.HIT:
                                                        libpkmon.player.addPokemon(libpkmon.Pokemon(
                                                                1, 15*500
                                                        ))
                                                        done = True
                                                elif hWnd == sele2 and msg == wmacros.HIT:
                                                        libpkmon.player.addPokemon(libpkmon.Pokemon(
                                                                4, 15*500
                                                        ))
                                                        done = True
                                                elif hWnd == sele3 and msg == wmacros.HIT:
                                                        libpkmon.player.addPokemon(libpkmon.Pokemon(
                                                                7, 15*500
                                                        ))
                                                        done = True
                                        pygame.display.flip()
                                        if done: break
                                break

                # Calling release to all present windows
                for i in wm: wm.DestroyWindow(i)

        elif result == load:
                pass

        # Main Scene
        import time
        fps = 0
        t = time.clock()


        # setBattle(uBattleNPCs)

        direction = []
        r_world = True     # render world if needed
        while True:
                evt.update()
                if evt.type == pygame.QUIT:
                        Release()
                        exit(0)
                screen.fill((0, 0, 0))

                if not uBattle.isRunning() and \
                                not uBackpack.isRunning() and \
                                not wm.isWindowPresent(uMe.ui) and \
                                not wm.isWindowPresent(uPokedex.ui):
                        r_world = True
                else:
                        r_world = False

                # render terrain to gaming world
                rgx, rgy = world.getTerrainRange()
                rgx, rgy = list(map(int, rgx)), list(map(int, rgy))
                (x0, x1), (y0, y1) = rgx, rgy
                if r_world:
                        terrain.render_s(world.getSurface(), world.Terrain2World(x0-2, y0-2), range(x0-2, x1+2), range(y0-2, y1+2))


                # check user event
                pManager.setTerrain(terrain)
                pManager.updateEvent(evt, wm)
                x = y = 0

                # check direction changes
                if not runningNpcEvent.isRunning() and \
                                not uMenu.isRunning() and \
                                not uBattle.isRunning() and \
                                not uBackpack.isRunning() and \
                                not wm.isWindowPresent(uMe.ui) and \
                                not wm.isWindowPresent(uPokedex.ui):


                        if evt.isKeyHit(pygame.K_UP):
                                direction.append(pygame.K_UP)
                        elif evt.isKeyHit(pygame.K_DOWN):
                                direction.append(pygame.K_DOWN)
                        elif evt.isKeyHit(pygame.K_LEFT):
                                direction.append(pygame.K_LEFT)
                        elif evt.isKeyHit(pygame.K_RIGHT):
                                direction.append(pygame.K_RIGHT)

                        try:
                                if evt.isKeyUp(pygame.K_UP):
                                        direction.remove(pygame.K_UP)
                                elif evt.isKeyUp(pygame.K_DOWN):
                                        direction.remove(pygame.K_DOWN)
                                elif evt.isKeyUp(pygame.K_LEFT):
                                        direction.remove(pygame.K_LEFT)
                                elif evt.isKeyUp(pygame.K_RIGHT):
                                        direction.remove(pygame.K_RIGHT)
                        except:
                                pass

                        if direction:
                                if direction[-1] == pygame.K_UP:
                                        y -= 1
                                elif direction[-1] == pygame.K_DOWN:
                                        y += 1
                                elif direction[-1] == pygame.K_LEFT:
                                        x -= 1
                                elif direction[-1] == pygame.K_RIGHT:
                                        x += 1
                                else:
                                        raise ValueError(direction[-1])
                else:
                        direction = []


                # check npc event
                player = pManager.getPlayer()
                player.normalize_pos()
                px, py = player.getPos()
                px+=x; py+=y

                # npc direction calc.
                di = base.DOWN
                if x > 0:
                        di = base.LEFT
                elif x < 0:
                        di = base.RIGHT
                elif y > 0:
                        di = base.UP

                # check npc event
                lidel = []
                for npc, bNpcEvent in npcManager.update(
                                pygame.Rect(rgx[0]-2, rgy[0]-2, rgx[1]-rgx[0]+4, rgy[1]-rgy[0]+4), (px, py)):
                        if bNpcEvent:
                                if not runningNpcEvent.isRunning() and npc.init(evt, wm):
                                        runningNpcEvent = npc
                                        npc.chgDir(di)
                                else:
                                        runningNpcEvent = base.NPC(None, None)
                        surf, pos = npc.render(evt, wm)
                        if surf is None:
                                lidel.append(npc)
                        else:
                                world.blit(surf, world.Terrain2World(*pos))

                for i in lidel:
                        npcManager.delete(i)

                # check player, fix the problem caused by launching 2 npc events during moving
                (surf, pos), pEvt, bMoving = pManager.update(x, y)
                if bMoving and runningNpcEvent.isRunning():
                        if pManager.getPlayer().cancelmove():
                                di = runningNpcEvent.getDir()
                                if di == base.UP: t = base.DOWN
                                elif di == base.DOWN: t = base.UP
                                elif di == base.LEFT: t = base.RIGHT
                                else: t = base.LEFT
                                pManager.getPlayer().chgDir(t)
                                (surf, pos), pEvt, bMoving = pManager.update(0, 0)
                if r_world:
                        world.blit(surf, world.Terrain2World(*pos))

                if pEvt != -1:
                        pEventList.append(pEvt[0](*pEvt[1]))
                        if not pEventList[-1].init(evt, wm): pEventList.pop()

                if r_world:
                        # shift world
                        x, y = ScreenSize
                        px, py = pos
                        px -= x/textureSize/2-0.5
                        py -= y/textureSize/2-0.5
                        world.setShift(px*textureSize, py*textureSize)
                        world.normalize()

                        # restrict view
                        r = g_cm.getRestriction()
                        if r is not None:
                                surf = pygame.Surface(world.getProjectionSize())
                                surf.fill((0, 0, 0))
                                x, y = world.Terrain2World(*pManager.getPlayer().getPos())
                                x -= world.getAbsoluteShift()[0]
                                y -= world.getAbsoluteShift()[1]
                                x += textureSize//2
                                y += textureSize//2
                                pygame.draw.circle(surf, (255, 255, 255), (int(x), int(y)), r, 0)
                                surf.set_colorkey((255, 255, 255))
                                world.blit(surf, world.getAbsoluteShift())

                        # render gaming world
                        if world.getSize()[0] > ScreenSize[0] and world.getSize()[1] > ScreenSize[1]: screen.blit(world.render_s(), (0, 0))
                        elif world.getSize()[1] > ScreenSize[1]: screen.blit(world.render_s(), ((ScreenSize[0]-world.getSize()[0])//2, 0))
                        elif world.getSize()[0] > ScreenSize[0]: screen.blit(world.render_s(), (0, (ScreenSize[1]-world.getSize()[1])//2))
                        else: screen.blit(world.render_s(), ((ScreenSize[0]-world.getSize()[0])//2, (ScreenSize[1]-world.getSize()[1])//2))

                # Player events
                for i in pEventList:
                        surf, pos = i.render(evt, wm)
                        if surf is None:
                                i.release(wm)
                                pEventList.remove(i)
                        else:
                                if isinstance(pos, (tuple, list)):
                                        screen.blit(surf, pos)

                # User Menu
                surf, pos = uMenu.update(evt, wm)
                if surf is not None:
                        if pos == menu.MENU_EXIT:
                                Release()
                                exit(0)
                        elif pos == menu.MENU_SAVE:
                                import wapisp
                                hPygameWindow = pygame.display.get_wm_info()["window"]
                                result, fname = wapisp.GetSaveFileName(hPygameWindow)
                                if result:
                                        try:
                                                pManager.getPlayer().save()
                                                with open(fname, "wb") as f:
                                                        pickle.dump(pManager.getPlayer(), f)
                                                pManager.getPlayer().load()
                                        except:
                                                pass
                                
                                
                                        
                                
                        elif pos == menu.MENU_LOAD:
                                import wapisp
                                hPygameWindow = pygame.display.get_wm_info()["window"]
                                result, fname = wapisp.GetOpenFileName(hPygameWindow)
                                if result:
                                        try:
                                                with open(fname, "rb") as f:
                                                        player = pickle.load(f)
                                                player.load()
                                                LoadPlayer(player)
                                                # pManager.getPlayer().load()
                                                # LoadMap(pManager.getPlayer().getPos())
                                        except:
                                                pass
                        uMenu.release(wm)

                # Battle
                if pManager.isBattleNeeded() and not uBattle.isRunning():
                        isWildWater = base.test(terrain.getProperty(*pManager.getPlayer().getPos()), 4)

                        if isWildWater:
                                if g_cm.getType() == maps.MAP_TYPE_GRASS: g_cm.setType(maps.MAP_TYPE_GRASSWATER)
                                elif g_cm.getType() == maps.MAP_TYPE_ROCK: g_cm.setType(maps.MAP_TYPE_ROCKWATER)
                        else:
                                if g_cm.getType() == maps.MAP_TYPE_GRASSWATER: g_cm.setType(maps.MAP_TYPE_GRASS)
                                elif g_cm.getType() == maps.MAP_TYPE_ROCKWATER: g_cm.setType(maps.MAP_TYPE_ROCK)
                        uBattle.setBackground(g_cm.getBattleBk())

                        uBattle.setFightingObjects(player, g_cm.getWildPlayer())
                        uBattle.init(evt, wm)
                elif evt.isKeyHit(pygame.K_0):
                        uBattle.release(wm)
                result = uBattle.render(evt, wm)[1]
                if result is not None and result != 0:
                        if result == battle.ATK:
                                # print("Winner: ATK, %s"%uBattle._atk.getCurrentPokemon().getName())
                                pass
                        elif result == battle.DEF:
                                # print("Winner: DEF, %s"%uBattle._def.getCurrentPokemon().getName())
                                pManager.getPlayer().setPos(107, 605)
                                pManager.getPlayer().money = 0
                                runningNpcEvent.release(wm)
                                for i in pManager.getPlayer().pokemon:
                                        i.load(i.tID, i.exp, i.name, changeid=i.id)
                                LoadMap(pManager.getPlayer().getPos())
                                pManager.getPlayer().chgDir(base.UP)
                        else:
                                raise ValueError(result)
                        uBattle.release(wm)

                # Backpack
                # if evt.isKeyHit(pygame.K_8) and not uBackpack.isRunning():
                # 	uBackpack.setPlayer(pManager.getPlayer())
                # 	uBackpack.init(evt, wm)
                # elif evt.isKeyHit(pygame.K_8):
                # 	uBackpack.release(wm)
                result = uBackpack.render(evt, wm)[1]
                if result is not None and result != 0:
                        uBackpack.release(wm)

                # WindowsManager should always stay above the world
                for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
                        screen.blit(surface, pos)

                # Present
                pygame.display.flip()

                if direction:
                        smap = mapManager.isSwitchMap(pManager.getPlayer().getPos(), direction[-1])
                        if smap is not None:
                                # print((smap, mapManager._link[tuple(pManager.getPlayer().getPos())]))
                                if direction[-1] == pygame.K_UP: pManager.getPlayer().chgDir(base.UP)
                                elif direction[-1] == pygame.K_DOWN: pManager.getPlayer().chgDir(base.DOWN)
                                elif direction[-1] == pygame.K_LEFT: pManager.getPlayer().chgDir(base.LEFT)
                                elif direction[-1] == pygame.K_RIGHT: pManager.getPlayer().chgDir(base.RIGHT)
                                pManager.getPlayer().setPos(*smap)
                                LoadMap(pManager.getPlayer().getPos())
                                direction = []

                fps += 1
                if time.clock() - t >= 1:
                        print(fps/(time.clock()-t))
                        fps = 0
                        t = time.clock()

        Release()

except Exception as err:
    # handle exceptions
        import sys, ctypes
        exc_type, exc_obj, exc_tb = sys.exc_info()
        user32 = ctypes.windll.LoadLibrary("user32.dll")
        user32.MessageBoxW(0,str(exc_type)+" at line: "+str(exc_tb.tb_lineno),"FATAL ERROR OCCURED",0x00000010|0x00000000|0x00001000|0x00010000|0x00040000)
        loader.release()
        try:Release()
        except Exception:pass
        try:pygame.quit()
        except Exception:pass
        raise rgine.exception.error(str(exc_type)+" at line: "+str(exc_tb.tb_lineno), Exception, logfile="CrashDump.log")
        exit(1)
