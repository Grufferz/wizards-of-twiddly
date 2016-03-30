import pygame, random, math, os, pickle
import wizards.constants
import time

class GameScreen(object):
    
    def __init__(self, world, collision, om, rm, tot_r, largest, bld, treasure_locations, level, pl_start, special_zones):
        super(GameScreen, self).__init__()
        random.seed(wizards.constants.NOW)
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 28)
        self.font1 = pygame.font.SysFont('Arial', 20)
        self.font2 = pygame.font.Font(None, 14)
        self.font3 = pygame.font.Font(None, 18)        

        # TODO Add level saving
        self.level = level
        self.level_score = random.randrange(1,7) + random.randrange(1,7)
        print("SCORE=" + str(self.level_score))
        
        self.world = world
        self.buildings = bld
        
        self.building_sprites = pygame.sprite.Group()
        self.building_sprites.empty()
        self.setup_buildings()
        
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.empty()
        self.add_tree_gfx()
        
        self.collision_map = collision
        self.object_map = om
     
        self.region_map = rm
        self.total_regions = tot_r
        self.largest_region = largest
        #print(str(self.total_regions)  + " > " + str(self.largest_region))

        #inventory manager
        self.im = wizards.inventory_manager.InventoryManager()
        
        # PLAYER INIT
        px = pl_start[0]
        py = pl_start[1]

        self.player_sprite = None
        self.player_sprite = pygame.sprite.Group()
        self.player_sprite.empty()

        # if player file exists load, if not create
        if os.path.isfile(wizards.constants.PL_FILE):
            #f = open(wizards.constants.PL_FILE, 'rb')
            self.pl = wizards.utils.load_zip(wizards.constants.PL_FILE)
            self.pl.x = px
            self.pl.y = py
            self.pl.init_image()
        else:
            # create player
            namer = wizards.name_maker.NameMaker()
            player_name = namer.generate_name()
            self.pl = wizards.player.Player(px, py, player_name)
            sword = self.im.add_sword_to_character()
            sword.set_owner(self.pl)
            potion = self.im.add_healing_potion()
            potion.set_owner(self.pl)

            self.pl.add_item_to_inventory(potion)
            self.pl.current_item = potion
            self.pl.add_item_to_inventory(sword)
            self.pl.set_current_weapon(sword)


        self.player_sprite.add(self.pl)
        self.player_moved = False


        self.special_zones = special_zones
        
        self.cursor_line = []
        self.cline2 = []
        
        self.accuracy = 0
        self.base_accuracy = 10
        self.monster_sprites = pygame.sprite.Group()
        self.magic_sprites = pygame.sprite.Group()
        self.fire_sprites = pygame.sprite.Group()
        
        self.turn = 0
        self.game_turn = 1
        
        self.mouse_down = False
        
        self.pop_up_visible = False
        
        # setup lit_map
        self.light = wizards.light_map.LightMap(self.collision_map)
        self.light.do_fov(self.pl.x, self.pl.y, self.pl.sight)       
        
        #place treasure
        self.treasure_map = [[0 for x in range(wizards.constants.WIDTH)] for y in range(wizards.constants.HEIGHT)]
        self.treasure_sprites = pygame.sprite.Group()
        self.treasure_locations = treasure_locations
        self.treasure_list = []
        # TODO Different treasure
        self.set_treasure()

        self.monster_map = [[0 for x in range(wizards.constants.WIDTH)] for y in range(wizards.constants.HEIGHT)]
        self.mons_gen = wizards.monster_gen.MonsterGenerator(self.level, self.monster_map, self.level_score)
        self.monster_list = []
        self.init_monsters_2(8)
        
        self.dmg_list = []

        self.temp_sprites = pygame.sprite.Group()
        
        self.dead_gfx = pygame.sprite.Group()
        #self.charm_gfx = pygame.sprite.Group()
        
        self.show_all_monsters = False

        
    def render(self, screen):
        screen.fill(wizards.constants.BLACK)
        
        if self.mouse_down:
            if len(self.cursor_line) > 0:
                c_list = pygame.sprite.Group()
                for p in self.cursor_line:
                    cx = p[0]
                    cy = p[1]
                    if self.collision_map[cy][cx] == 1:
                        break
                    temp_block = wizards.cursor_blocks.CursorBlocks(cx,cy)
                    c_list.add(temp_block)
                c_list.draw(screen)
            
        self.building_sprites.draw(screen)
        self.all_sprite_list.draw(screen)
           
        #monsters
        for mons in self.monster_sprites.sprites():
            if self.light.lit(mons.x, mons.y) or self.show_all_monsters:
                if not mons.dead:
                    screen.blit(mons.image, (mons.rect.x,mons.rect.y))
                    
        #charmed gfx
        #self.charm_gfx.draw(screen)
        for mons in self.monster_list:
            if mons.charmed and not mons.dead and self.light.lit(mons.x, mons.y):
                screen.blit(mons.charm_gfx.image, (mons.charm_gfx.x,mons.charm_gfx.y))                    
        
        self.fire_sprites.draw(screen)
        
        self.magic_sprites.draw(screen)
        
        pygame.draw.rect(screen, wizards.constants.WHITE, (0,wizards.constants.MSGBOX_TOP,wizards.constants.MSGBOX_W,wizards.constants.MSGBOX_H))
        
        text1 = self.font1.render('Current Spell: ' + self.pl.cur_spell.name, True, wizards.constants.BLACK)
        #target = self.get_item_cursor()
        text2 = self.font1.render('XP: ' + str(self.pl.xp), True, wizards.constants.BLACK)

        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        mx, my = self.convert_screen_pos_to_grid(mouse_x,mouse_y)          
        d = self.get_distance(self.pl.x, self.pl.y,mx, my)
        d2 = 0
        if len(self.cursor_line) > 0:
            tmp = self.cursor_line[-1]
            tx = tmp[0] #* constants.CHAR_SIZE
            ty = tmp[1] #* constants.CHAR_SIZE            
            d2 = self.get_distance(self.pl.x, self.pl.y,tx, ty)

        ds = 'Distance: ' + str(d) + "(" + str(d2)+ ")"
        text3 = self.font1.render(ds, True, wizards.constants.BLACK)

        text24 = self.font1.render("Item: " + self.pl.get_current_item_string(), True, wizards.constants.BLACK)
                
        screen.blit(text1, (wizards.constants.MSG_GUT_1,wizards.constants.MSGBOX_TOP+8))
        screen.blit(text2, (wizards.constants.MSG_GUT_1,wizards.constants.MSGBOX_TOP+32))
        screen.blit(text24, (wizards.constants.MSG_GUT_2, wizards.constants.MSGBOX_TOP + 8))
        screen.blit(text3, (wizards.constants.MSG_GUT_2,wizards.constants.MSGBOX_TOP+32))
        
        start = self.pl.get_pos_tuple()
        end = (mx,my)
        self.cline2 = wizards.utils.get_line(start,end)
        
        if len(self.cline2) > 0:
            text4 = self.font1.render('SEE: ' + str(self.can_see_target(self.cline2)), True, wizards.constants.BLACK)
            screen.blit(text4, (wizards.constants.MSG_GUT_3,wizards.constants.MSGBOX_TOP+32))
            
        text5 = self.font1.render('Turn: ' + str(self.game_turn), True, wizards.constants.BLACK)
        screen.blit(text5, (wizards.constants.MSG_GUT_3,wizards.constants.MSGBOX_TOP+8))

        # Display item in square
        itemid = self.cell_contains_item(self.pl.x, self.pl.y)
        if itemid > 0:
            item = self.get_item_by_id(itemid)
            text6 = self.font1.render('Item: ' + item.itemname, True, wizards.constants.BLACK)
            screen.blit(text6, (wizards.constants.MSG_GUT_2,wizards.constants.MSGBOX_TOP+8))
        
        #magic box
        pygame.draw.rect(screen, wizards.constants.MAG_DB, (wizards.constants.MB_BACK_L,wizards.constants.MB_BACK_T,wizards.constants.MB_BACK_W,wizards.constants.MB_BACK_H))

        #get magic percent
        m_perc = self.pl.get_magic_percent()
        m_box_w = int(wizards.constants.MAGIC_BOX_W * (m_perc/100))
        
        pygame.draw.rect(screen, wizards.constants.MAG_BLUE, (wizards.constants.MAGIC_BOX_LEFT,wizards.constants.MAGIC_BOX_TOP,m_box_w,wizards.constants.MAGIC_BOX_H))
        
        magic_text = self.font3.render('Mana: ' + str(self.pl.magic), True, wizards.constants.WHITE)
        screen.blit(magic_text, (wizards.constants.MAGIC_BOX_LEFT + 10,wizards.constants.MAGIC_BOX_TOP+2))
        
        #health box
        pygame.draw.rect(screen, wizards.constants.HB_BACK, (wizards.constants.HB_BACK_L,wizards.constants.HB_BACK_T,wizards.constants.HB_BACK_W,wizards.constants.HB_BACK_H))
        
        h_perc = self.pl.get_hp_percent()
        h_box_w = int(wizards.constants.HEALTH_BOX_W * (h_perc/100))
        
        pygame.draw.rect(screen, wizards.constants.HB_RED, (wizards.constants.HEALTH_BOX_LEFT,wizards.constants.HEALTH_BOX_TOP,h_box_w,wizards.constants.HEALTH_BOX_H))
        
        health_text = self.font3.render('Health: ' + str(self.pl.hp), True, wizards.constants.WHITE)
        screen.blit(health_text, (wizards.constants.HEALTH_BOX_LEFT + 10,wizards.constants.HEALTH_BOX_TOP+2))
                
        
        #damage
        kill_list = []
        for dmg in self.dmg_list:
            d_text = self.font2.render(str(dmg.d), True, wizards.constants.WHITE)
            screen.blit(d_text, (dmg.x*wizards.constants.CHAR_SIZE+10,dmg.y*wizards.constants.CHAR_SIZE))
            if self.turn % 2:
                dmg.y -= 1
            if dmg.y < 0:
                kill_list.append(dmg)
        for kl in kill_list:
            self.dmg_list.remove(kl)
            
        
        #dead gfx
        for dgfx in self.dead_gfx.sprites():
            #dgfx.rect.x -= 2
            #dgfx.rect.y -= 2
            #dgfx.image = pygame.transform.smoothscale(dgfx.image, (dgfx.scale_x, dgfx.scale_y))
            #dgfx.rect = dgfx.image.get_rect()
            if dgfx.zoomfactor > 1:
                #dgfx.image = pygame.transform.rotozoom(dgfx.img_orig, 0, dgfx.zoomfactor)
                tmp = dgfx.image
                oldrect = tmp.get_rect()
                tmp = pygame.transform.smoothscale(dgfx.img_orig, (dgfx.zoomfactor, dgfx.zoomfactor))
                newrect = tmp.get_rect()
                tx = dgfx.x
                ty = dgfx.y
                tx += int(oldrect.centerx - newrect.centerx)
                ty += int(oldrect.centery - newrect.centery)
                screen.blit(tmp, (tx,ty))
            
        #self.dead_gfx.draw(screen)
        
        # treasure sprites
        self.treasure_sprites.draw(screen)
        self.player_sprite.draw(screen)
        # self.temp_sprites.draw(screen)
                
        #pop up box
        
        if self.pop_up_visible:
            player_quad = self.select_quadrant(self.pl.rect.x, self.pl.rect.y)
            
            self.display_msg_box(screen, player_quad, "Hello!")
            
        #test for FOV
        #for y in range(constants.FHEIGHT):
            #for x in range(constants.FWIDTH):
                #print(str(y) + "_" + str(x))
               # print(str(self.light.lit(x,y)))
                #if self.light.lit(x, y):
                    #screen.blit(self.pl.image, (x*constants.CHAR_SIZE, y*constants.CHAR_SIZE))
                    
        
    
    def update(self):
        self.turn += 1
        
        #kill off dead monsters
        kill_list = []
        for mons in self.monster_list:
            if mons.dead == True:
                kill_list.append(mons)
                self.collision_map[mons.y][mons.x] = 0
                self.monster_map[mons.y][mons.x] = 0
                dgfx = wizards.dead_gfx.DeadGraphic(mons.x, mons.y)
                self.dead_gfx.add(dgfx)
        
        for kl in kill_list:
            self.monster_list.remove(kl)
            self.monster_sprites.remove(kl)
            
        #update dead gfx
        kill_list = []
        for dgfx in self.dead_gfx.sprites():
            if dgfx.lifespan > 0:
                dgfx.lifespan -= 1
                dgfx.zoomfactor += 2
            else:
                kill_list.append(dgfx)
        for kl in kill_list:
            self.dead_gfx.remove(kl)
        
        self.magic_sprites.update()
        self.fire_sprites.update()
        if len(self.fire_sprites) > 0:
            remove_list = []
            for brn in self.fire_sprites.sprites():

                #burn up
                if brn.resistance < 10 and brn.removed == False:
                    brn.removed = True
                    tup = (brn.x,brn.y)
                    remove_list.append(tup) 
                    t = wizards.tree.Tree(brn.x,brn.y)
                    for tr in self.all_sprite_list.sprites():
                        if tr.x == brn.x and tr.y == brn.y:
                            self.all_sprite_list.remove(tr)
                    
            for rm in remove_list:
                rx = rm[0]
                ry = rm[1]
                self.world[ry][rx] == 0
                cx = (rx * wizards.constants.F_BLOCKS) // wizards.constants.CHAR_SIZE
                cy = (ry * wizards.constants.F_BLOCKS) // wizards.constants.CHAR_SIZE
                self.collision_map[cy][cx] = 0
                
                
    def handle_events(self, events):
        moveLeft = moveRight = moveUp = moveDown = pick_up =  False
        magic_cast = False
        
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.manager.go_to(wizards.title_screen.TitleScreen())
                elif e.key == pygame.K_w:
                    moveUp = True
                    moveDown = False
                elif e.key == pygame.K_q:
                    moveUp = True
                    moveLeft = False
                    moveDown = False
                    moveRight = True
                elif e.key == pygame.K_e:
                    moveUp = True
                    moveLeft = True
                    moveDown = False
                    moveRight = False
                elif e.key == pygame.K_x or e.key == pygame.K_s:
                    moveUp = False
                    moveDown = True
                elif e.key == pygame.K_a:
                    moveLeft = True
                    moveRight = False
                elif e.key == pygame.K_d:
                    moveRight = True
                    moveLeft = False
                elif e.key == pygame.K_c:
                    moveUp = False
                    moveLeft = True
                    moveDown = True
                    moveRight = False
                elif e.key == pygame.K_z:
                    moveUp = False
                    moveLeft = False
                    moveDown = True
                    moveRight = True
                elif e.key == pygame.K_p:
                    pick_up = True
                elif e.key == pygame.K_n:
                    self.cycle_spell()
                elif e.key == pygame.K_LEFTBRACKET:
                    self.pl.cycle_cur_item_up()
                elif e.key == pygame.K_RIGHTBRACKET:
                    self.pl.cycle_cur_item_down()
                elif e.key == pygame.K_m:
                    self.toggle_msg_box()
                elif e.key == pygame.K_l:
                    if self.show_all_monsters:
                        self.show_all_monsters = False
                    else:
                        self.show_all_monsters = True
            
            lastmovetime = time.time() - 1
            
            mx = 0
            my = 0 
            
            del self.cursor_line[:]
            
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            mx, my = self.convert_screen_pos_to_grid(mouse_x,mouse_y)   

            start = self.pl.get_pos_tuple()
            end = (mx,my)
            self.cursor_line = self.block_list(wizards.utils.get_line(start,end))
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                
                self.mouse_down = True

                if len(self.cursor_line) > 0:
                    tmp = self.cursor_line[-1]
                    tx = tmp[0] * wizards.constants.CHAR_SIZE
                    ty = tmp[1] * wizards.constants.CHAR_SIZE
                    
                    #has player enough magic?
                    
                    if self.pl.can_cast_spell(self.pl.cur_spell.magic_cost):
                        
                        magic_cast = True
                        self.player_moved = True
                        
                        #check accuracy

                        # TODO Add max range to spells

                        dis = self.get_distance(start[0],start[1],tmp[0],tmp[1])
                        dis_mod = self.get_distance_mod(dis)
                        self.accuracy = self.base_accuracy + dis_mod
                        hit = self.ranged_combat(self.accuracy)

                        # TODO Abstract ranged combat a bit more
                        
                        #if miss change hit location
                        if not hit:
                            base_miss = random.randrange(1,4) + dis_mod
                            hmod_x = base_miss * wizards.constants.CHAR_SIZE
                            hmod_y = base_miss * wizards.constants.CHAR_SIZE
                            if random.randrange(10) > 4:
                                rmod = 1
                            else:
                                rmod = -1
                            tx += (hmod_x * rmod)
                            ty += (hmod_y * rmod)
                            
                            #get new line
                            start = self.pl.get_pos_tuple()
                            nx,ny = self.convert_screen_pos_to_grid(mouse_x,mouse_y)  
                            end = (nx,ny)
                            self.cursor_line = self.block_list(wizards.utils.get_line(start,end))
                            
                            tmp = self.cursor_line[-1]
                            tx = tmp[0] * wizards.constants.CHAR_SIZE
                            ty = tmp[1] * wizards.constants.CHAR_SIZE
                            
                        #check what sort of spell
                        #fireball = 1
                        if self.pl.cur_spell.spell_type == 1:
                            self.create_magic_explosion(tx // wizards.constants.CHAR_SIZE,ty // wizards.constants.CHAR_SIZE)
                            tiny_tup = self.convert_screen_pos_to_tiny_grid(tx,ty)
                            tiny_x = tiny_tup[0]
                            tiny_y = tiny_tup[1]
                            
                            burn_list = self.get_burnt_list(tiny_x,tiny_y,self.pl.cur_spell.radius)
                            
                            explosion_list = self.get_radius_list(tiny_x,tiny_y,self.pl.cur_spell.radius)
                            
                            grid_list = []
                            for bl in burn_list:
                                self.set_tree_on_fire(bl[0],bl[1])
                            #damage monsters
                            for el in explosion_list:
                                grid_pos = self.convert_small_to_big(el[0],el[1])
                                if grid_pos not in grid_list:
                                    grid_list.append(grid_pos)  
                            
                            for gp in grid_list:
                                ex_x = gp[0]
                                ex_y = gp[1]
                                for monster in self.monster_list:
                                    #print(str(monster.x) + " >> " + str(ex_x))
                                    # saving throw
                                    roll = random.randrange(20) + 1
                                    if monster.x == ex_x and monster.y == ex_y and (roll < monster.save_magic):
                                        #print(monster.name)
                                        # take damage
                                        dmg = random.randrange(1,self.pl.cur_spell.damage)
                                        monster.take_damage(dmg)
                                        # create damage graphic
                                        dm_token = wizards.damage_token.DamageToken(monster.x, monster.y-10, dmg)
                                        self.dmg_list.append(dm_token)
                                        # if monster dead add xp
                                        cr = wizards.resolve_combat.CombatResolver()
                                        xp = cr.get_xp_for_monster(monster.level)
                                        self.pl.add_xp(xp)

                        # charm spell
                        elif self.pl.cur_spell.spell_type == 2:
                            self.create_magic_explosion(tx // wizards.constants.CHAR_SIZE,ty // wizards.constants.CHAR_SIZE)
                            tiny_tup = self.convert_screen_pos_to_tiny_grid(tx,ty)
                            tiny_x = tiny_tup[0]
                            tiny_y = tiny_tup[1]
                            
                            grid_list = []
                            explosion_list = self.get_radius_list(tiny_x,tiny_y,self.pl.cur_spell.radius)
                            for el in explosion_list:
                                grid_pos = self.convert_small_to_big(el[0],el[1])
                                if grid_pos not in grid_list:
                                    grid_list.append(grid_pos)  
                            
                            for gp in grid_list:
                                ex_x = gp[0]
                                ex_y = gp[1]
                                for monster in self.monster_list:
                                    if monster.x == ex_x and monster.y == ex_y and monster.charmable:
                                        ch = self.test_charm(monster.save_magic)
                                        if ch:
                                            #xp = monster.rect.centerx
                                            #yp = monster.rect.centery
                                            monster.charmed = True
                                            monster.charmed_by = self.pl
                                            xp = monster.rect.x - 4
                                            yp = monster.rect.y - 4
                                            c = wizards.charmed_gfx.Charmed(xp,yp)
                                            monster.charm_gfx = c
                                            #self.charm_gfx.add(c)
                        
                        #use magic
                        self.pl.deplete_magic(self.pl.cur_spell.magic_cost)
                                
            else:
                self.mouse_down = False
            
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_w:
                    moveUp = False
                elif e.key == pygame.K_x:
                    moveDown = False
                elif e.key == pygame.K_a:
                    moveLeft = False
                elif e.key == pygame.K_d:
                    moveRight = False
                elif e.key == pygame.K_q:
                    moveUp = False
                    moveLeft = False
                elif e.key == pygame.K_e:
                    moveUp = False
                    moveRight = False
                elif e.key == pygame.K_c:
                    moveDown = False
                    moveRight = False
                elif e.key == pygame.K_z:
                    moveDown = False
                    moveLeft = False
                elif e.key == pygame.K_p:
                    pick_up = False

                    
            if time.time() - 0.5 > lastmovetime:

                # TODO If monster dies, drop treasure

                # move up
                if moveUp and not moveLeft and not moveRight and not moveDown:
                    if self.cell_contains_monster(self.pl.x, self.pl.y-1) == 0:
                        if not self.is_in_exit_zone(self.pl.x, self.pl.y-1):
                            self.pl.updatePlayer(0,self.collision_map)
                            self.player_moved = True
                        else:
                            self.clean_up()
                            self.manager.go_to(wizards.exit_level_screen.ExitScreen(self.pl, self.level, 1))
                    else:
                        mid = self.cell_contains_monster(self.pl.x, self.pl.y-1)
                        mons = self.get_monster_by_id(mid)
                        combat_resolver = wizards.resolve_combat.CombatResolver()
                        dmg = combat_resolver.resolve_player_hit(self.pl, mons)
                        dm_token = wizards.damage_token.DamageToken(mons.x, mons.y - 10, dmg)
                        self.dmg_list.append(dm_token)
                        self.player_moved = True
                # move down
                elif moveDown and not moveLeft and not moveRight and not moveUp:
                    if self.cell_contains_monster(self.pl.x, self.pl.y + 1) == 0:
                        if not self.is_in_exit_zone(self.pl.x, self.pl.y + 1):
                            self.pl.updatePlayer(2,self.collision_map)
                            self.player_moved = True
                        else:
                            self.clean_up()
                            self.manager.go_to(wizards.exit_level_screen.ExitScreen(self.pl, self.level, 2))
                    else:
                        mid = self.cell_contains_monster(self.pl.x, self.pl.y + 1)
                        mons = self.get_monster_by_id(mid)
                        combat_resolver = wizards.resolve_combat.CombatResolver()
                        dmg = combat_resolver.resolve_player_hit(self.pl, mons)
                        dm_token = wizards.damage_token.DamageToken(mons.x, mons.y - 10, dmg)
                        self.dmg_list.append(dm_token)
                        self.player_moved = True
                # move left
                elif moveLeft and not moveUp and not moveDown and not moveRight:
                    if self.cell_contains_monster(self.pl.x-1, self.pl.y) == 0:
                        if not self.is_in_exit_zone(self.pl.x-1, self.pl.y):
                            self.pl.updatePlayer(3,self.collision_map)
                            self.player_moved = True
                        else:
                            self.clean_up()
                            self.manager.go_to(wizards.exit_level_screen.ExitScreen(self.pl, self.level, 1))
                    else:
                        mid = self.cell_contains_monster(self.pl.x-1, self.pl.y)
                        mons = self.get_monster_by_id(mid)
                        combat_resolver = wizards.resolve_combat.CombatResolver()
                        dmg = combat_resolver.resolve_player_hit(self.pl, mons)
                        dm_token = wizards.damage_token.DamageToken(mons.x, mons.y - 10, dmg)
                        self.dmg_list.append(dm_token)
                        self.player_moved = True
                # move right
                elif moveRight and not moveUp and not moveDown and not moveLeft:
                    if self.cell_contains_monster(self.pl.x + 1, self.pl.y) == 0:
                        if not self.is_in_exit_zone(self.pl.x + 1, self.pl.y):
                            self.pl.updatePlayer(1,self.collision_map)
                            self.player_moved = True
                        else:
                            self.clean_up()
                            self.manager.go_to(wizards.exit_level_screen.ExitScreen(self.pl, self.level, 1))
                    else:
                        mid = self.cell_contains_monster(self.pl.x + 1, self.pl.y)
                        mons = self.get_monster_by_id(mid)
                        combat_resolver = wizards.resolve_combat.CombatResolver()
                        dmg = combat_resolver.resolve_player_hit(self.pl, mons)
                        dm_token = wizards.damage_token.DamageToken(mons.x, mons.y - 10, dmg)
                        self.dmg_list.append(dm_token)
                        self.player_moved = True
                # move NW
                elif moveRight and moveUp and not moveDown and not moveLeft:
                    if self.cell_contains_monster(self.pl.x - 1, self.pl.y - 1) == 0:
                        if not self.is_in_exit_zone(self.pl.x - 1, self.pl.y - 1):
                            self.pl.updatePlayer(7, self.collision_map)
                            self.player_moved = True
                        else:
                            self.clean_up()
                            self.manager.go_to(wizards.exit_level_screen.ExitScreen(self.pl, self.level, 1))
                    else:
                        mid = self.cell_contains_monster(self.pl.x - 1, self.pl.y - 1)
                        mons = self.get_monster_by_id(mid)
                        combat_resolver = wizards.resolve_combat.CombatResolver()
                        dmg = combat_resolver.resolve_player_hit(self.pl, mons)
                        dm_token = wizards.damage_token.DamageToken(mons.x, mons.y - 10, dmg)
                        self.dmg_list.append(dm_token)
                        self.player_moved = True
                # move NE
                elif moveLeft and moveUp and not moveDown and not moveRight:
                    if self.cell_contains_monster(self.pl.x + 1, self.pl.y - 1) == 0:
                        if not self.is_in_exit_zone(self.pl.x + 1, self.pl.y - 1):
                            self.pl.updatePlayer(4, self.collision_map)
                            self.player_moved = True
                        else:
                            self.clean_up()
                            self.manager.go_to(wizards.exit_level_screen.ExitScreen(self.pl, self.level, 1))
                    else:
                        mid = self.cell_contains_monster(self.pl.x + 1, self.pl.y - 1)
                        mons = self.get_monster_by_id(mid)
                        combat_resolver = wizards.resolve_combat.CombatResolver()
                        dmg = combat_resolver.resolve_player_hit(self.pl, mons)
                        dm_token = wizards.damage_token.DamageToken(mons.x, mons.y - 10, dmg)
                        self.dmg_list.append(dm_token)
                        self.player_moved = True
                # move SE
                elif moveDown and moveLeft and not moveUp and not moveRight:
                    if self.cell_contains_monster(self.pl.x + 1, self.pl.y + 1) == 0:
                        if not self.is_in_exit_zone(self.pl.x + 1, self.pl.y + 1):
                            self.pl.updatePlayer(5, self.collision_map)
                            self.player_moved = True
                        else:
                            self.clean_up()
                            self.manager.go_to(wizards.exit_level_screen.ExitScreen(self.pl, self.level, 2))
                    else:
                        mid = self.cell_contains_monster(self.pl.x + 1, self.pl.y + 1)
                        mons = self.get_monster_by_id(mid)
                        combat_resolver = wizards.resolve_combat.CombatResolver()
                        dmg = combat_resolver.resolve_player_hit(self.pl, mons)
                        dm_token = wizards.damage_token.DamageToken(mons.x, mons.y - 10, dmg)
                        self.dmg_list.append(dm_token)
                        self.player_moved = True
                # move SW
                elif moveDown and moveRight and not moveUp and not moveLeft:
                    if self.cell_contains_monster(self.pl.x - 1, self.pl.y + 1) == 0:
                        if not self.is_in_exit_zone(self.pl.x - 1, self.pl.y + 1):
                            self.pl.updatePlayer(6, self.collision_map)
                            self.player_moved = True
                        else:
                            self.clean_up()
                            self.manager.go_to(wizards.exit_level_screen.ExitScreen(self.pl, self.level, 2))
                    else:
                        mid = self.cell_contains_monster(self.pl.x - 1, self.pl.y + 1)
                        mons = self.get_monster_by_id(mid)
                        combat_resolver = wizards.resolve_combat.CombatResolver()
                        dmg = combat_resolver.resolve_player_hit(self.pl, mons)
                        dm_token = wizards.damage_token.DamageToken(mons.x, mons.y - 10, dmg)
                        self.dmg_list.append(dm_token)
                        self.player_moved = True
                # pick up item if we are standing on one
                elif pick_up:
                    item_id = self.cell_contains_item(self.pl.x, self.pl.y)
                    if item_id > 0:
                        item = self.get_item_by_id(item_id)
                        item.set_owner(self.pl)
                        self.pl.add_item_to_inventory(item)
                        self.pl.add_xp(item.value)
                        self.treasure_map[self.pl.y][self.pl.x] = 0
                        self.treasure_sprites.remove(item)





                # restore magic
                if not magic_cast and self.player_moved == True:
                    self.pl.restore_magic(self.pl.magic_restore)
                    
                lastmovetime = time.time()
                if self.player_moved:
                    self.player_moved = False
                    self.game_turn += 1
                    self.light.do_fov(self.pl.x, self.pl.y, self.pl.sight)
    
    def add_tree_gfx(self):
        for y in range(wizards.constants.FHEIGHT):
            for x in range(wizards.constants.FWIDTH):
                if self.world[y][x] == 1:
                    t = wizards.tree.Tree(x,y)
                    self.all_sprite_list.add(t)
     
    def setup_buildings(self):
        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                if self.buildings[y][x] == 1:
                    t = wizards.wall.WallSprite(x,y)
                    self.building_sprites.add(t)
                    
                    
    def get_player_start(self):
        l = []
        #for y in range(constants.HEIGHT):
        y = wizards.constants.HEIGHT - 3
        for x in range(wizards.constants.WIDTH):
            if self.collision_map[y][x] == 0 and self.in_largest_region(x,y):
                tup = (x,y)
                l.append(tup)
                    
        t = random.choice(l)
        return t
    
    def get_monster_start(self):
        sx = random.randrange(wizards.constants.WIDTH)
        sy = random.randrange(wizards.constants.HEIGHT)
        while self.collision_map[sy][sx] == 1:
            sx = random.randrange(wizards.constants.WIDTH)
            sy = random.randrange(wizards.constants.HEIGHT)
            
        return (sx,sy)
            
                        
    #def setup_collision_map(self):
        #for y in range(constants.FHEIGHT):
            #for x in range(constants.FWIDTH):
                #if self.world[y][x] == 1:
                    #xp = int((x*constants.F_BLOCKS) / constants.CHAR_SIZE)
                    #yp = int((y*constants.F_BLOCKS) / constants.CHAR_SIZE)
                    #self.collision_map[yp][xp] = 1        
                    
    def convert_screen_pos_to_grid(self,mx,my):
        x = mx // wizards.constants.CHAR_SIZE
        y = my // wizards.constants.CHAR_SIZE
        return x, y
    
    def convert_screen_pos_to_tiny_grid(self,mx,my):
        x = mx // wizards.constants.F_BLOCKS
        y = my // wizards.constants.F_BLOCKS
        return x, y    

    def convert_small_to_big(self,sx,sy):
        bx = (sx * wizards.constants.F_BLOCKS) // wizards.constants.CHAR_SIZE
        by = (sy * wizards.constants.F_BLOCKS) // wizards.constants.CHAR_SIZE
        return (bx, by)
    
    def select_quadrant(self, pl_x, pl_y):
        x = pl_x // 640
        y = pl_y // 360
       
        rv = None
        if x == 0 and y == 0:
            rv = 0
        elif x == 0 and y == 1:
            rv = 2
        elif x == 1 and y == 0:
            rv = 1
        elif x == 1 and y == 1:
            rv = 3
        return rv

    def create_magic_explosion(self, x, y):
        num = random.randrange(8) + 4
        for i in range(num):
            mag = wizards.magic_spell.MagicSpell(x,y)
            self.magic_sprites.add(mag)
            
    
    def block_list(self, lst):
        #returns part of list if blocked
        counter = 0
        ret_list = []
        for l in lst:
            lx = l[0]
            ly = l[1]
            if lx >= 0 and ly >= 0 and lx < wizards.constants.WIDTH and ly < wizards.constants.HEIGHT:
                if self.collision_map[ly][lx] == 1:
                   # print("BLOCKED!")
                    ret_list = lst[:counter]
                    return ret_list
                else:
                    counter += 1
        return lst
    
    #def populate_objects(self):
        #for y in range(constants.FHEIGHT):
            #for x in range(constants.FWIDTH):
                #if self.world[y][x] == 1:
                    #f = game_objects.FireEffect(25.0)
                    #self.object_map[y][x] = game_objects.TreeWood(x,y,f)
                    
    
    def set_tree_on_fire(self, x, y):
        #print(str(x) + " _ " + str(y))
        burn = wizards.game_objects.Heat(2.0, 2.0)
        res = random.uniform(0.0, 20.0) + 70.0
        fe = wizards.game_objects.FireEffect(res)
        burn_tree = wizards.game_objects.BurningTree(x,y,fe,burn)
        self.object_map[y][x] = burn_tree
        tree_sprite = wizards.burning_tree_sprite.BurningTreeSprite(x,y,burn_tree.fire_effect.resistance,burn_tree.heat.intensity )
        self.fire_sprites.add(tree_sprite)
        
        
    def set_next_tree_on_fire(self, x, y, inten):
        burn = wizards.game_objects.Heat(inten, 2.0)
        res = random.uniform(0.0, 20.0) + 70.0
        fe = wizards.game_objects.FireEffect(res)
        burn_tree = wizards.game_objects.BurningTree(x,y,fe,burn)
        self.object_map[y][x] = burn_tree
        tree_sprite = wizards.burning_tree_sprite.BurningTreeSprite(x,y,burn_tree.fire_effect.resistance,burn_tree.heat.intensity )
        self.fire_sprites.add(tree_sprite)    
    
    def get_burnt_list(self, xc, yc, rad):
        min_x = max(0, xc - rad)
        max_x = min(wizards.constants.FWIDTH-1, xc + 1)
        
        min_y = max(0, yc - rad)
        max_y = min(wizards.constants.FHEIGHT-1, yc + 1)
        
        ret_list = []
        
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if ((x - xc)*(x - xc) + (y - yc)*(y - yc) <= rad*rad):
                    xsym = xc - (x - xc)
                    ysym = yc - (y - yc)
                    if self.valid_move(xsym,ysym):
                        if self.object_map[ysym][xsym].flammable:
                            ret_list.append((xsym,ysym))
                    if self.valid_move(x,y):
                        if self.object_map[y][x].flammable:
                            ret_list.append((x,y))
                    if self.valid_move(x,ysym):
                        if self.object_map[ysym][x].flammable:
                            ret_list.append((x,ysym))
                    if self.valid_move(xsym,y):
                        if self.object_map[y][xsym].flammable:
                            ret_list.append((xsym,y))
                    
        return ret_list
    
    
    def get_radius_list(self, xc, yc, rad):
        min_x = max(0, xc - rad)
        max_x = min(wizards.constants.FWIDTH-1, xc + 1)
        
        min_y = max(0, yc - rad)
        max_y = min(wizards.constants.FHEIGHT-1, yc + 1)
        
        ret_list = []
        
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if ((x - xc)*(x - xc) + (y - yc)*(y - yc) <= rad*rad):
                    xsym = xc - (x - xc)
                    ysym = yc - (y - yc)
                    if self.valid_move(xsym,ysym):
                        ret_list.append((xsym,ysym))
                    if self.valid_move(x,y):
                        ret_list.append((x,y))
                    if self.valid_move(x,ysym):
                        ret_list.append((x,ysym))
                    if self.valid_move(xsym,y):
                        ret_list.append((xsym,y))
                    
        return ret_list
    
    
    def valid_move(self, x, y):
        if x < 0 and y < 0:
            return False
        elif x >= wizards.constants.FWIDTH or y >= wizards.constants.FHEIGHT:
            return False
        else:
            return True
    
    def find_monster_by_loc(self, x, y):
        for monster in self.monster_list:
            if monster.x == x and monster.y == y:
                return monster
        return None
        

    def get_item_cursor(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        mx, my = self.convert_screen_pos_to_tiny_grid(mouse_x,mouse_y)  
        bigx, bigy = self.convert_screen_pos_to_grid(mouse_x,mouse_y)
        if mx < 0:
            mx = 0
        if my < 0:
            my = 0
        if mx >= wizards.constants.FWIDTH:
            mx = wizards.constants.FWIDTH-1
        if my >= wizards.constants.FHEIGHT:
            my = wizards.constants.FHEIGHT-1
        #monster = self.find_monster_by_loc(bigx,bigy)
        #print(str(monster))
        fm = None
        for monster in self.monster_list:
            if monster.x == bigx and monster.y == bigy:
                fm = monster
        if fm is not None:
            return fm.name
        else:
            item = self.object_map[my][mx].name
            return item
    
    def get_distance(self, x1, y1, x2, y2):
        d = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        return d
    
    def get_h_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)    
    
    def can_see_target(self, path):
        for p in path:
            px = p[0]
            py = p[1]
            if not self.is_valid_grid_pos(px,py):
                return False
            if self.collision_map[py][px] == 1:
                return False
        return True
        
    def is_valid_grid_pos(self,x,y):
        return x >= 0 and y >= 0 and x < wizards.constants.WIDTH and y < wizards.constants.HEIGHT
    
    
    def get_distance_mod(self, dis):
        dm = 0 
        if dis > wizards.constants.DIS_PENALTY:
            dm = (dis-wizards.constants.DIS_PENALTY) // 10
        return dm
    
    def ranged_combat(self,dis_mod):
        roll = 0 
        for i in range(3):
            roll += random.randrange(6)+1
        if roll >= 17 or roll >= dis_mod:
            return True
        else:
            return False
        
    def get_walls(self):
        retlist = []
        for y in range(wizards.constants.HEIGHT):
            for x in range(wizards.constants.WIDTH):
                if self.collision_map[y][x] == 1:
                    t = (x, y)
                    retlist.append(t)   
        return retlist     
    
    def is_lit(self,x,y):
        return self.light.lit(x,y)
    
    def is_colliding(self,x,y):
        if self.collision_map[y][x] == 1:
            return True
        else:
            return False
        
    def is_too_near(self,x,y,l,dist):
        for li in l:
            if self.get_distance(x,y,li[0],li[1]) <= dist:
                return True
        return False
    
    def in_largest_region(self,x,y):
        return self.region_map[y][x] == self.largest_region
            
    
    def init_monsters_2(self, num_mons):
        positions = []

        for i in range(num_mons):
            start_pos = self.get_monster_start()
            while self.is_lit(start_pos[0],start_pos[1]) or self.is_too_near(start_pos[0],start_pos[1],positions,10) or not self.in_largest_region(start_pos[0],start_pos[1]):
                start_pos = self.get_monster_start()
            positions.append(start_pos)
        
        self.monster_list = self.mons_gen.return_monster_list(positions, self.im, 1)
        
        for m in self.monster_list:
            self.monster_sprites.add(m)
                
    
    #def init_monsters(self, num_mons):
        ##grid = square_grid.SquareGrid(constants.WIDTH,constants.HEIGHT)
        ##grid.walls = self.get_walls()
        
        #player_pos = (self.pl.x, self.pl.y)
        
        #mons_gen = monster_gen.MonsterGenerator(self.level)
        
        #for i in range(num_mons):
            #start_pos = self.get_monster_start()
            #sx = start_pos[0]
            #sy = start_pos[1]
            #reg = self.region_map[sy][sx]
            #h_distance = self.get_h_distance(sx, sy, self.pl.x, self.pl.y)
            
            ##came_from, cost = a_star.a_star_search(grid,start_pos,player_pos)
            ##if len(came_from) > 0:
                ##path = a_star.reconstruct_path(came_from,start_pos,player_pos)
                ##print(str(len(path)))
                
            ##check not in player's sight, not too close and not trapped
            #while self.light.lit(sx,sy) or reg != self.largest_region or (sx != self.pl.x and sy != self.pl.y) or h_distance < 20:
                #start_pos = self.get_monster_start()
                #sx = start_pos[0]
                #sy = start_pos[1]  
                #reg = self.region_map[sy][sx]
                #h_distance = self.get_h_distance(sx, sy, self.pl.x, self.pl.y)
            
            #o = mons_gen.return_single_monster(sx,sy)
            #self.collision_map[sy][sx] = 1 
            #self.monster_sprites.add(o)
            #self.monster_list.append(o)
            
            
            
    def cycle_spell(self):
        cur_spell = self.pl.spell_index
        if len(self.pl.spell_list) > 1:
            next_spell = cur_spell + 1
            if next_spell >= len(self.pl.spell_list):
                next_spell = 0
            self.pl.cur_spell = self.pl.spell_list[next_spell]
            self.pl.spell_index = next_spell
            
    def test_charm(self, resist):
        roll = random.randrange(20)+1
        if roll >= 17 or roll > resist:
            return True
        else:
            return False   
        

    def display_msg_box(self, scr, q, msg):
  
        pbl = wizards.constants.PB_LEFT_GUT
        pbt = wizards.constants.PB_TOP_GUT
        pbw = wizards.constants.PB_WIDTH
        pbh = wizards.constants.PB_HEIGHT
        
        if q == 0:
            pbl += wizards.constants.PB_LEFT_DIV
        elif q == 2:
            pbl += wizards.constants.PB_LEFT_DIV
            #pbt += constants.PB_TOP_DIV
            
        pygame.draw.rect(scr, wizards.constants.GREY, (pbl-10,pbt-10,pbw+20,pbh+20))
        pygame.draw.rect(scr, wizards.constants.WHITE, (pbl,pbt,pbw,pbh))
        d_text = self.font1.render(msg, True, wizards.constants.BLACK)
        scr.blit(d_text, (pbl+10,pbt+10))   
        
    def toggle_msg_box(self):
        if self.pop_up_visible == True:
            self.pop_up_visible = False
        elif self.pop_up_visible == False:
            self.pop_up_visible = True
        
    def set_treasure(self):
        
        sq = wizards.square_grid.SquareGrid(wizards.constants.WIDTH,wizards.constants.HEIGHT)
        sq.walls = self.get_walls()
        pl_start = (self.pl.x,self.pl.y)
        dis_map = wizards.searches.breadth_first_search(sq,pl_start)
        max_val = 0
        add_list = []
        for key,v in dis_map.items():
            if v > max_val:
                max_val = v
        for key, v in dis_map.items():
            if v > (max_val-40):
                add_list.append(key)
                #t = temp_gfx.TempGraphic(key[0],key[1])
                #self.temp_sprites.add(t)                  
            #print(str(key[0]))
        self.treasure_locations = self.treasure_locations + add_list
        
        num_treasures = random.randrange(1,self.level_score+1)

        placed_treasure = []
        for l in range(num_treasures):
            loc = random.choice(self.treasure_locations)
            if len(placed_treasure) < 1:
                placed_treasure.append(loc)
            else:
                while self.is_too_near(loc[0],loc[1],placed_treasure,20):
                    loc = random.choice(self.treasure_locations)
                placed_treasure.append(loc)

        for treasure in placed_treasure:
            #t = self.im.add_gold(treasure[0],treasure[1], self.treasure_map)
            t = self.im.add_potion_with_location(treasure[0], treasure[1], self.treasure_map)
            self.treasure_list.append(t)
            self.treasure_sprites.add(t)

    def cell_contains_monster(self, x, y):
        return self.monster_map[y][x]

    def cell_contains_item(self, x, y):
        return self.treasure_map[y][x]

    def get_item_by_id(self, number):
        for treasure in self.treasure_list:
            if treasure.item_id == number:
                return treasure
        return None

    def get_monster_by_id(self, number):
        for monster in self.monster_list:
            if monster.monster_id == number:
                return monster
        return None

    def resolve_hand_combat(self, monster_id):
        monster = self.get_monster_by_id(monster_id)
        resolver = wizards.CombatResolver()
        # TODO Melee combat for monsters

    def is_in_exit_zone(self, x, y):
        tup = (y, x)
        if tup in self.special_zones:
            return True
        else:
            return False

    def clean_up(self):
        self.player_sprite.empty()
        self.all_sprite_list.empty()
        self.building_sprites.empty()
        self.monster_sprites.empty()
        self.magic_sprites.empty()
        self.fire_sprites.empty()
        self.treasure_sprites.empty()
        self.temp_sprites.empty()
        self.dead_gfx.empty()




