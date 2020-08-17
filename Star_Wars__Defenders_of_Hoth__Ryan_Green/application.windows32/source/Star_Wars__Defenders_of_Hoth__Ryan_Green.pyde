"""
                                                        Star Wars - Defenders of Hoth
                                                           Created By:  Ryan Green
"""
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-  Data Map  -~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#   Name            Purpose                                                                                 Type            Limit
##  shipcor         Holds the ship's coordinates as [x, y]                                                  List            n/a
##  tiecor          Holds the enemy ship's coordinates [x, y]                                               List            n/a
##  shooting        Holds if the player is shooting                                                         Boolean         True or False
##  plntlife        Holds the planet's remaining life                                                       int             0 - 5
##  lasercooldown   Holds the laser's cooldown timer                                                        int             1 - 254
##  plyrinfo        Holds information about the player [[Name, Score], Difficulty, Selected, Letter Index]  List            n/a
##  mode            Holds the mode                                                                          str             "Menu", "Play", or "G. Over"
##  starjedi        Holds the font                                                                          Font            n/a
##  rot             Holds menu background's rotation                                                        int             >= 0
##  characters      Holds the possible characters for a name                                                List            n/a
##  movie           Holds the intro video file                                                              Movie           n/a
##  streak          Holds the player's killstreak                                                           int             >= 0
##  norml           Holds the dictionary of highscores for the normal difficulty; loaded from file          Dictionary      n/a
##  hard            Holds the dictionary of highscores for the hard difficulty; loaded from file            Dictionary      n/a
##  movie           Holds the holds the intro video                                                         Movie           n/a
##  dstarmv         Holds x and y increments of the Death Star                                              List            [1 or -1, 1 or -1]
##  dstarcor        Holds current coordinates of the Death Star [x,y]                                       List            n/a
##  minim           Initializes the minim library                                                           Minim           n/a
##  sounds          Holds the sounds that were loaded                                                       List            n/a
##  imgs            Holds all of the loaded images                                                          Dictionary      n/a
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

add_library('minim')

add_library('Video')

import random
import pickle

def setup():
    global shooting, shipcor, tiecor, plntlife, lasercooldown, plyrinfo, mode, starjedi, rot, characters, movie, streak, norml, hard, dstarmv, dstarcor, sounds, minim, imgs
    
    size( 800, 600 )
    
    shipcor, tiecor, shooting, plntlife, lasercooldown, rot, mode, plyrinfo, streak, norml, hard = reset()
    #plyrinfo = [[["A", "A", "A"], 0], 1, 0, 0] #[[Name, Score], Difficulty, Selected, Letter Index]
    
    cursor(loadImage( "Cursor.gif" ))
    starjedi = loadFont( "StarJediRounded-48.vlw" )
    characters = ["A", "B", "C", "D", "E", "F", "G", "H", "i", "J", "K", "L", "M", "N", "o", "P", "q", "R", "S", "T", "u", "v", "w", "x", "Y", "z", "#", "$", "%", "&", "*"]
    movie = Movie( this, "Intro.mp4" )
    textFont( starjedi )
    dstarmv = [1, 1]
    dstarcor = [700, 400, 1]
    minim = Minim(this)
    sounds = [minim.loadFile("Spring-Boing.wav"), minim.loadFile("Laser.wav"), minim.loadFile("Shield Down.wav"), minim.loadFile("8-Bit Star Wars.wav"), minim.loadFile("Blip_Select25.wav"), minim.loadFile("Porg.mp3"), minim.loadFile("Explosion.wav"),  minim.loadFile("Sound1.wav")   ] # Boing, Laser, Shield Break, Music 2 Loop, Select Sound, Letter, Porg, Explosion
    imgs = { "falcon" : loadImage("Falcon.png"), "laser" : loadImage("Saber.png"), "back" : loadImage("Hoth.jpeg"), "tie" : loadImage("TieFighter.png"), "explosion" : loadImage("Explosion.png"), "shield" : loadImage("EnergyShield.png"), "shieldcrack" : loadImage("cracks.png"), "logo" : loadImage("Star Wars.png"), "deathstar" : loadImage("Death_Star.png"), "paused" : loadImage("Paused.png"), "porg" : loadImage("PorgHelp.png")}
    sounds[ 3 ].loop()


def draw():
    global shooting, shipcor, tiecor, plntlife, lasercooldown, plyrinfo, mode, starjedi, rot, characters, streak, norml, hard, dstarmv, dstarcor, sounds, minim, imgs
    
    if mode == "Menu":
        
        rot = menuback( rot, imgs["back"] )
        
        imageMode(CENTER)
        image(imgs["logo"], 400, 150, imgs["logo"].width / 1.05, imgs["logo"].height / 1.05)
        
        
        textAlign( CENTER )
        textSize( 48 )
    
        if (335 <= mouseX <= 480) and (275 <= mouseY <= 310):
            fill( 98, 198, 250 )
            text( "Play", 397, 297 )
            
        fill(255, 255, 255)
        text( "Play", 400, 300 )
        
        
        for n in range( 3 ):
            if plyrinfo[ 2 ] == n:
                fill(98, 198, 250)
            else:
                fill( 255, 255, 255 )
                
            text( plyrinfo[ 0 ][ 0 ][ n ], 350 + (50 * n), 450 )
        #-----------------END OF FOR LOOP-----------------
        
        textSize(20)
        fill( 162, 249, 0 )
        text( "By: Ryan Green", 700, 25 )
        
        textSize(28)
        
        if ( 110 <= mouseX <= 300 ) and ( 360 <= mouseY <= 380 ):
            fill( 98, 198, 250 )
            text( "Highscores", 198, 368 )
        
        fill( 255, 255, 255 )
        text( "Highscores", 200, 370 )
        
        if (520 <= mouseX <= 700) and (360 <= mouseY <= 380):
            fill( 98, 198, 250 )
            text( "Difficulty", 598, 368 )
    
        fill( 255, 255, 255 )
        text( "Difficulty", 600, 370 )
        
        if (570 <= mouseX <= 645) and (540 <= mouseY <= 560):
            fill( 98, 198, 250 )
            text( "Exit", 598, 548 )
        
        fill( 255, 255, 255 )
        text( "Exit", 600, 550 )
    
        image(imgs["porg"], 86.8 , 546.6, imgs["porg"].width / 10.0, imgs["porg"].height / 10.0)
        
    #--------------------------------------------~Menu Ends Here~--------------------------------------------        
    
    elif mode == "Play":
    
        imageMode(CORNER)
        background = image(imgs["back"], -15, -10, imgs["back"].width / 1.5, imgs["back"].height / 1.5)
        imageMode(CENTER)
        
        tiecor[ 0 ] -= (5 * plyrinfo[ 1 ]) + (plyrinfo[ 0 ][ 1 ] / 1000.0) # Tie Fighter
        tiecor[ 1 ] += (3 * plyrinfo[ 1 ]) + (plyrinfo[ 0 ][ 1 ] / 1000.0) #  Movement
        
        image(imgs["tie"], tiecor[ 0 ], tiecor[ 1 ], imgs["tie"].width / 6.0, imgs["tie"].height / 6.0)
        """
        # HitBox Test
        fill( 255, 255, 255 )
        rect(tiecor[ 0 ] - imgs["tie"].width / 12.0, tiecor[ 1 ] - imgs["tie"].height / 12.0, (tiecor[ 0 ] + imgs["tie"].width / 12.0)- (tiecor[ 0 ] - imgs["tie"].width / 12.0), (tiecor[ 1 ] + imgs["tie"].height / 12.0) - (tiecor[ 1 ] - imgs["tie"].height / 12.0))
        fill( 255, 0, 0 )
        rect((shipcor[ 0 ] + 85 + imgs["falcon"].width / 8.0 - imgs["laser"].width / 4.0), (shipcor[ 1 ] - 15), (shipcor[ 0 ] + imgs["falcon"].width / 8.0 + imgs["laser"].width / 4.0) - (shipcor[ 0 ] + 85 + imgs["falcon"].width / 8.0 - imgs["laser"].width / 4.0), (shipcor[ 1 ] + 15) - (shipcor[ 1 ] - 15))
        """
        
        if shooting:
            for y in range(int(tiecor[ 1 ] - imgs["tie"].height / 12.0), int(tiecor[ 1 ] + imgs["tie"].height / 12.0)):
                if ((shipcor[ 1 ] - 15) <= y < (shipcor[ 1 ] + 15)):
                    for x in range(int(tiecor[ 0 ] - imgs["tie"].width / 12.0), int(tiecor[ 0 ] + imgs["tie"].width / 12.0)):
                        if  ((shipcor[ 0 ] + 85 + imgs["falcon"].width / 8.0 - imgs["laser"].width / 4.0) <= x < (shipcor[ 0 ] + imgs["falcon"].width / 8.0 + imgs["laser"].width / 4.0)):
                    
                            image(imgs["explosion"], tiecor[ 0 ], tiecor[ 1 ], imgs["explosion"].width / 3.0, imgs["explosion"].height / 3.0)
                            playsounds(sounds, 6, minim)
                            cor = tieReset(tiecor)
                            plyrinfo[ 0 ][ 1 ] += (5 * plyrinfo[ 1 ]) + streak
                            streak += 1
                            y = "STOP"
                            break
                        #-----------------END OF IF STATEMENT-----------------
                    if y == "STOP":
                        break
                    #-----------------END OF 2nd FOR LOOP-----------------
                #-----------------END OF 2nd IF-----------------
            #-----------------END OF 1st FOR LOOP-----------------
         #-----------------END OF 1st IF-----------------                   
        
        if (tiecor[ 0 ] <= (0 - imgs["tie"].width / 12.0)) or (tiecor[ 1 ] >= (600 + imgs["tie"].height / 12.0)):
            plntlife -= 1
            cor = tieReset(tiecor)
            playsounds(sounds, 2, minim)
            streak = 0
   
        
        pushMatrix()
        if not(mouseY in range(shipcor[ 1 ] - imgs["falcon"].height / 16, shipcor[ 1 ] + imgs["falcon"].height / 16)):
            translate(shipcor[ 0 ], shipcor[ 1 ])
            if mouseY > (shipcor[ 1 ] + imgs["falcon"].height / 16):
                rotate(radians(2.5))
            elif mouseY < (shipcor[ 1 ] - imgs["falcon"].height / 16):
                rotate(radians(-0.95))
            
            if shooting:
                image(imgs["laser"], 25 + imgs["falcon"].width / 8.0, - 5, imgs["laser"].width/2.0, imgs["laser"].height/2.0)
            image(imgs["falcon"], 0, 0, imgs["falcon"].width / 8.0, imgs["falcon"].height / 8.0)
    
        else:
            if shooting:
                image(imgs["laser"], shipcor[ 0 ] + 25 + imgs["falcon"].width / 8.0, shipcor[ 1 ] - 5, imgs["laser"].width/2.0, imgs["laser"].height/2.0)
    
            image(imgs["falcon"], shipcor[ 0 ], shipcor[ 1 ], imgs["falcon"].width / 8.0, imgs["falcon"].height / 8.0)
        popMatrix()
        
        for n in range(plntlife): # Lives
            image(imgs["shield"], 675 - (n*55), 550, imgs["shield"].width / 5.0, imgs["shield"].height / 5.0)
         
         # Shooting + Cooldown
         # vvvvvvvvvvvvvvvvvvv
            
        fill( 65, 127, 160 )
        rect( 12, 12, 106, 31 )
        fill( 98, 198, 250 ) 
        rect( 15, 15, (lasercooldown / 250.0)*100 , 25 )
        
        if 15 < lasercooldown > 25:
            shooting = False
            
        textSize(12)
        if lasercooldown < 250:
            lasercooldown += 5
        else:
            fill( 0, random.randint( 0, 50 ), random.randint( 0, 200 ))
            text( "Recharged!", 65, 30.5 )
        
        textAlign(LEFT)
        fill( 255, 215, 0 )
        text( "Score: %s"%plyrinfo[ 0 ][ 1 ], 10, 595 ) # Score Display
        textAlign(CENTER)
        
        
        if plntlife == 0: # Game Over Check; Checks if no lives, then sorts and writes scores to file
            mode = "G. Over"
            if plyrinfo[ 1 ] == 1:
                norml = sorter(norml, plyrinfo[ 0 ])

                with open('normal.txt', 'wb') as f:
                    pickle.dump(norml, f, protocol=2)
                f.close()
            
            else:
                hard = sorter(hard, plyrinfo[ 0 ])

                with open('hard.txt', 'wb') as f:
                    pickle.dump(hard, f, protocol=2)
                f.close()
        
        pausebttn() # Draws Pause Button
            
    #--------------------------------------------~Play Ends Here~--------------------------------------------        
    
    elif mode == "G. Over":
        
        imageMode(CORNER)
        background = image(imgs["back"], -15, -10, imgs["back"].width / 1.5, imgs["back"].height / 1.5)
        imageMode(CENTER)
        
        # Draws Broken Shield
        image(imgs["shieldcrack"], 250, 400, imgs["shieldcrack"].width / 1.5, imgs["shieldcrack"].height / 1.5)
        
        pushMatrix()
        translate( 175, 425 )
        rotate(radians(60))
        image(imgs["shieldcrack"], 15, 5, imgs["shieldcrack"].width , imgs["shieldcrack"].height )
        image(imgs["shieldcrack"], 2, 15, imgs["shieldcrack"].width / 1.9, imgs["shieldcrack"].height / 1.9)
        popMatrix()
        # --------------------------------------------------------------
        
        fill( 147, 9, 27 )
        textSize(40)
        text( "Game over\r\n Shield Breached", 575, 500 )
        
        textSize(30)
        textAlign(RIGHT)
        text( "Score: %s"%plyrinfo[ 0 ][ 1 ], 790, 40 )
        
        textAlign(CENTER)
        if (70 < mouseX < 345) and (135 < mouseY < 158):
            fill( 255, 9, 27 )
            text( "Return to Menu", 199, 149 )
            fill( 147, 9, 27 )
            
        text( "Return to Menu", 200, 150 )
     
    #--------------------------------------------~Game Over Ends Here~--------------------------------------------  
              
    elif mode == "Intro":
        
        image(movie, 400, 300, movie.width / 1.7, movie.height / 1.7) # Draws Frames of the Video
        
        textAlign(LEFT)
        textSize(10)
        fill( 147, 147, 147 )
        text( "Click Anywhere to Continue", 5, 10 )
        textAlign(CENTER)
    
    elif mode == "Scores":
        rot = menuback(rot, imgs["back"])
        
        textAlign(CENTER)
        textSize(35)
        fill( 255, 215, 0 )
        text( "Normal\nDifficulty", 250, 150 )
        text( "Hard\nDifficulty", 550, 150 )
        fill( 255, 255, 255 )
        textSize(30)
        for n in range(1,6):
            text( "%s:    %s"%( norml[ n ][ 0 ], norml[ n ][ 1 ] ), 250, 175 + ( n * 50 ) ) # Normal Score Display
            text( "%s:    %s"%( hard[ n ][ 0 ], hard[ n ][ 1 ] ), 550, 175 + ( n * 50 ) )   # Hard Score Display
        
        rtn2mnu(mode) # Draws Return Button
    
    elif mode == "Difficulty": 
            
        dstarcor[ 0 ] += dstarmv[ 0 ] # x-increment for the Death Star
        dstarcor[ 1 ] += dstarmv[ 1 ] # y-increment for the Death Star
    
        pushMatrix()
        translate(dstarcor[ 0 ], dstarcor[ 1 ])
        scale(dstarcor[ 2 ], 1)
        image(imgs["deathstar"], 0, 0, imgs["deathstar"].width / 12.0, imgs["deathstar"].height / 12.0)
        popMatrix()
    
        # Death Star Bouncing
        
        if (dstarcor[ 0 ] + dstarmv[ 0 ] + imgs["deathstar"].width / 24.0) >= 800: # Right Side
            dstarcor[ 0 ] += 800 - dstarcor[ 0 ] -  imgs["deathstar"].width / 24.0 + dstarmv[ 0 ]
            dstarmv[ 0 ] *= -1
            dstarcor[ 2 ] *= -1
            playsounds(sounds, 0, minim)
        
        elif (dstarcor[ 0 ] + dstarmv[ 0 ] - imgs["deathstar"].width / 24.0) <= 0: # Left Side
            dstarcor[ 0 ] += 0 - dstarcor[ 0 ] +  imgs["deathstar"].width / 24.0  + dstarmv[ 0 ]
            dstarmv[ 0 ] *= -1
            dstarcor[ 2 ] *= -1
            playsounds(sounds, 0, minim)
        
        if (dstarcor[ 1 ] + dstarmv[ 1 ] + imgs["deathstar"].height / 24.0) >= 600: # Bottom
            dstarcor[ 1 ] += 600 - dstarcor[ 1 ] -  imgs["deathstar"].height / 24.0 + dstarmv[ 1 ]
            dstarmv[ 1 ] *= -1
            playsounds(sounds, 0, minim)
        
        elif (dstarcor[ 1 ] + dstarmv[ 1 ] - imgs["deathstar"].height / 24.0) <= 0: # Top
            dstarmv, dstarcor = starbelow(0, dstarcor, dstarmv, imgs["deathstar"].height)
            playsounds(sounds, 0, minim)
    
    
        if (0 < dstarcor[ 1 ] < 243):
        
            if (dstarcor[ 0 ] < 300) and (dstarcor[ 0 ] + dstarmv[ 0 ] + imgs["deathstar"].width / 24.0) >= 206: # Left of Logo
                dstarcor[ 0 ] += 206 - dstarcor[ 0 ] -  imgs["deathstar"].width / 24.0 + dstarmv[ 0 ]
                dstarmv[ 0 ] *= -1
                dstarcor[ 2 ] *= -1
                playsounds(sounds, 0, minim)
        
            elif (dstarcor[ 0 ] > 500) and (dstarcor[ 0 ] + dstarmv[ 0 ] - imgs["deathstar"].width / 24.0) <= 577: # Right of Logo
                dstarcor[ 0 ] += 577 - dstarcor[ 0 ] +  imgs["deathstar"].width / 24.0  + dstarmv[ 0 ]
                dstarmv[ 0 ] *= -1
                dstarcor[ 2 ] *= -1
                playsounds(sounds, 0, minim)
    
        elif (206 < dstarcor[ 0 ] < 577):
        
            if (dstarcor[ 1 ] + dstarmv[ 1 ] - imgs["deathstar"].height / 24.0) <= 243: # Bottom of Logo
                dstarmv, dstarcor = starbelow(243, dstarcor, dstarmv, imgs["deathstar"].height)
                playsounds(sounds, 0, minim)
        
        rectMode(CENTER)
    
        
        
        fill( 255, 215, 0 )
        text( "Difficulty:", 405, 300 )
        
        fill( 255, 215, 0 )
        if plyrinfo[ 1 ] == 1:
            fill( 98, 198, 250 )
            
        elif not(( 195 < mouseX < 360 ) and ( 345 < mouseY < 365 )):
            fill( 255, 255, 255 )
    
        text( "Normal", 250, 355 )
        
        fill( 255, 215, 0 )
        if plyrinfo[ 1 ] == 2:
            fill( 98, 198, 250 )

        elif not((515 < mouseX < 605) and (345 < mouseY < 365)):
            fill( 255, 255, 255 )
    
        text( "Hard", 550, 355 )    
        rectMode(CORNER)
        
        rtn2mnu(mode) # Draws Return Button
    
    #--------------------------------------------~Difficulty Ends Here~--------------------------------------------    
                
    elif mode == "Paused":
        
        imageMode(CORNER)
        background = image(imgs["paused"], 0, 0, imgs["paused"].width * 1.2, imgs["paused"].height * 1.2 )
        
        textSize(45)

        text( "Paused", 400, 150 )   
        
        pausebttn() # Draws Pause Button
          
        rtn2mnu(mode) # Draws Return Button
    
    elif mode == "Help":
        rot = menuback(rot, imgs["back"])
        rtn2mnu(mode) # Draws Return Button
        # Instructions vvvvvvv
        textAlign(CENTER)
        textSize(35)
        fill( 255,215,0 )
        text( "Getting\nStarted", 250, 135 )
        text( "Gameplay", 550, 150 )
        fill( 255, 255, 255 )
        
        textSize(30)
        text( "on the menu screen use WASD to choose your name. When you are ready, press play to begin.", 150, 175, 200, 500 )
        
        text( "While playing, use WASD to move your ship and left click to shoot. You can pause with the button in bottom right corner of the screen.", 400, 175, 300, 500 )
 
               
def movieEvent(m): # Used to draw each frame of the intro
    m.read()

def tieReset(cor): # Recieves the Tie Fighter's Coordinates
    # Generates Starting Coordinates for the next Tie Fighter
    # Returns the Tie Fighter's Coordinates
    cor[ 0 ] = random.randint(1200, 1500)
    cor[ 1 ] = random.randint(-500, -100)
    return(cor)
    
def reset(): # Resets (or sets) the variables after each game
    # Loads the dictionaries from normal.txt and hard.txt
    # Returns the (re)set variables
    shipcor = [100, 400]
    tiecor = [1300, -300]
    shooting = False
    plntlife = 7
    lasercooldown = 250
    rot = 0
    mode = "Menu"
    plyrinfo = [[["A", "A", "A"], 0], 1, 0, 0]
    streak = 0
    
    file = open( "normal.txt", 'rb' ) # read in binary
    norml = pickle.load( file )
    file.close()

    file = open( "hard.txt", 'rb' ) # read in binary
    hard = pickle.load( file )
    file.close()
    
    return(shipcor, tiecor, shooting, plntlife, lasercooldown, rot, mode, plyrinfo, streak, norml, hard)

def sorter(changer, plyrsvinfo): # Receives the required dictionary and the player info
    # Compares and sorts the player's score into the highscores
    # Returns the specified dictionary
    for n in range(1,6):
        
        if plyrsvinfo[ 1 ] > int(changer[ n ][ 1 ]):
            temp = [""] * (5)
            for x in range(1, 6):
                temp[x-1] = changer[x]
        
            temp.insert(n-1, plyrsvinfo)
            temp.pop(5)

            for n in range(5):
                changer[n+1] = temp.pop(0)
            break
    return(changer)

def menuback(rotatr, bck): # Recieves the rotation and the background image
    # Draws the Rotating Main Menu and Highscore screen background
    # Returns the rotation
    fill( 0, 0, 0 )
    for n in range(0, 501, 500):
        rect(0, n, 800, 100)
    
    imageMode(CORNER)
    pushMatrix()
    translate(400, 300)
    rotate(radians(rotatr))
    image(bck, -455, -910, bck.width * 1.5, bck.height * 1.5)
    popMatrix()
    imageMode(CENTER)
        
    rotatr += 0.1
    return(rotatr)

def starbelow(blw, cor, mov, hght): # Recieves the Y value that the ball is below,
                                    # the Death Star's Coordinates, the Death Star's
                                    # Movement, and the Death Star's Height
    # Finds if the Death Star will be above the specified point, moves it to that point
    # changes direction
    # Returns the Death Star's movement and coordinates
    if (cor[ 1 ] + mov[ 1 ] - hght / 24.0) <= blw:
            cor[ 1 ] += blw - cor[ 1 ] +  hght / 24.0 + mov[ 1 ]
            mov[ 1 ] *= -1
    return(mov, cor)
    
def rtn2mnu(mde): # Receives the mode
    # Draws the Return to menu button
    # Draws the Highlighting if the Button is Hovered Over
    # Returns Nothing (as no variables are changed
    if (( mouseX in range( 340, 475 )) and ( mouseY in range( 485, 535 ))) and (( mode == "Scores" ) or ( mode == "Paused" ) or ( mode == "Help" )) :
        fill( 98, 198, 250 )
        text( "Return\ntoMenu", 398, 498 )

    if (( mouseX in range( 340, 475 )) and ( mouseY in range( 485, 535 ))) and ( mode == "Difficulty" ):    
        fill( 98, 198, 250 )
    else:
        
        fill( 255, 255, 255 )
    text( "Return\ntoMenu", 400, 500 )
    return()

def playsounds(snds, num, minim ): # Receives the List of Sounds, the Index to Play, and minim variable
    
    snds[ num ].play() # Plays specified sound
    snds[ num ].rewind() # Rewinds sound for next use
    
    return() # Returns nothing as no variables were changed

def pausebttn(): 
    
    for n in range( 3 ): # Draws the Menu Button
        fill( 255, 255, 255 )
        rect(715, 525 + (20 * n), 60, 15, 20)
    
    return() # Returns nothing as no variables were changed

def keyPressed():
    global shipcor, mode, plyrinfo, characters, imgs
    
    if mode == "Play":
        # Ship Movement vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        if key in ['W', 'w'] and shipcor[ 1 ] >= (0 + imgs["falcon"].height / 16.0):
            shipcor[ 1 ] -= 2
            
        elif key in ['S', 's'] and shipcor[ 1 ] <= (600 - imgs["falcon"].height / 16.0):
            shipcor[ 1 ] += 2
            
        elif key in ['A', 'a'] and shipcor[ 0 ] >= (-5 + imgs["falcon"].width / 16.0):
            shipcor[ 0 ] -= 2
            
        elif key in ['D', 'd'] and shipcor[ 0 ] <= (350 - imgs["falcon"].width / 16.0):
            shipcor[ 0 ] += 2
    #--------------------------------------------~Play Ends Here~--------------------------------------------
    elif mode == "Menu":
        # Name Selection VVVVVV
        if key in [ 'W', 'w' ]:
            if (plyrinfo[ 3 ] - 1) == -1:
                plyrinfo[ 3 ] = 30
            else:
                plyrinfo[ 3 ] -= 1
            
            plyrinfo[ 0 ][ 0 ][plyrinfo[ 2 ]] = characters[ plyrinfo[ 3 ] ]
            playsounds(sounds, 7, minim)
        
        elif key in ['S', 's']:
            if (plyrinfo[ 3 ] + 1) == 31:
                plyrinfo[ 3 ] = 0
            else:
                plyrinfo[ 3 ] += 1
            
            playsounds(sounds, 7, minim)
            plyrinfo[ 0 ][ 0 ][plyrinfo[ 2 ]] = characters[ plyrinfo[ 3 ] ]
            
        elif key in ['A', 'a']:
            if plyrinfo[ 2 ] == 0:
                plyrinfo[ 2 ] = 2
            else:
                plyrinfo[ 2 ] -= 1
                
            playsounds(sounds, 7, minim)
            plyrinfo[ 3 ] = characters.index(plyrinfo[ 0 ][ 0 ][plyrinfo[ 2 ]])
        
        elif key in ['D', 'd']:
            if plyrinfo[ 2 ] == 2:
                plyrinfo[ 2 ] = 0
            else:
                plyrinfo[ 2 ] += 1
                
            playsounds(sounds, 7, minim)
            plyrinfo[ 3 ] = characters.index( plyrinfo[ 0 ][ 0 ][ plyrinfo[ 2 ] ])
    #--------------------------------------------~Menu Ends Here~-------------------------------------------- 
            

        
            
def mousePressed():
    global shipcor, tiecor, shooting, plntlife, lasercooldown, rot, mode, plyrinfo, movie, streak, norml, hard, sounds, minim
    
    if mode == "Menu":
        if (335 <= mouseX < 480) and (275 <= mouseY < 310): # Play Button
            mode = "Intro"
            playsounds(sounds, 4, minim)
            sounds[ 3 ].pause()
            plyrinfo[ 0 ][ 0 ] = "".join(plyrinfo[ 0 ][ 0 ])
            plntlife = 7 - (plyrinfo[ 1 ] * 2 )
            movie.play()
        
        elif (570 <= mouseX <= 645) and (540 <= mouseY <= 560): # Exit Button
            playsounds(sounds, 4, minim)
            sounds[ 3 ].pause()
            exit()
        
        elif (110 <= mouseX < 300) and (360 <= mouseY < 375): # Highscores Button
            playsounds(sounds, 4, minim)
            mode = "Scores"
            
        elif (520 <= mouseX <= 700) and (360 <= mouseY <= 380): # Difficulty Button
            playsounds(sounds, 4, minim)
            mode = "Difficulty"
            rot = menuback(rot, imgs["back"])
            image(imgs["logo"], 400, 150, imgs["logo"].width / 1.05, imgs["logo"].height / 1.05)
            
        elif (mouseX <= 180) and (mouseY >= 493):
            playsounds(sounds, 5, minim)
            mode = "Help"
    #--------------------------------------------~Menu Ends Here~--------------------------------------------        
   
    elif mode == "Play":
        if (725 <= mouseX <= 790) and (535 <= mouseY <= 590): # Pause Button
            playsounds(sounds, 4, minim)
            mode = "Paused"
        
        elif lasercooldown >= 250: # Shooting
            playsounds(sounds, 1, minim)
            shooting = True
            lasercooldown = 1
    #--------------------------------------------~Play Ends Here~--------------------------------------------    
    
    elif mode == "G. Over":
        if (70 < mouseX < 345) and (135 < mouseY < 158): # Return to Menu Button
            playsounds(sounds, 4, minim)
            shipcor, tiecor, shooting, plntlife, lasercooldown, rot, mode, plyrinfo, streak, norml, hard = reset()
    #--------------------------------------------~Game Over Ends Here~--------------------------------------------    
    
    elif mode == "Intro": # Intro; Click to Continue
        movie.stop()
        sounds[ 3 ].loop()
        mode = "Play"
        
    
    elif mode == "Scores":
        if (340 <= mouseX < 475) and (485 <= mouseY <= 535): # Return to Menu from Highscores
            playsounds(sounds, 4, minim)
            mode = "Menu"
            
    elif mode == "Difficulty":
        if (195 < mouseX < 360) and (345 < mouseY < 365): # Normal Button
            plyrinfo[ 1 ] = 1
            playsounds(sounds, 4, minim)
            
        elif (515 < mouseX < 605) and (345 < mouseY < 365): # Hard Button
            plyrinfo[ 1 ] = 2
            playsounds(sounds, 4, minim)
        
        elif (340 <= mouseX < 475) and (485 <= mouseY < 535): # Return to Menu from Difficulty
            mode = "Menu"
            playsounds(sounds, 4, minim)
    #--------------------------------------------~Difficulty Ends Here~--------------------------------------------        
    
    elif mode == "Paused":
        if (725 <= mouseX <= 790) and (535 <= mouseY <= 590): # Unpause Button
            mode = "Play"
            playsounds(sounds, 4, minim)
        
        elif (340 <= mouseX < 475) and (485 <= mouseY < 535): # Return to Menu from Paused
            mode = "Play"
            plntlife = 0
            playsounds(sounds, 4, minim)
    #--------------------------------------------~Paused Ends Here~--------------------------------------------
                    
    elif mode == "Help":
        if (340 <= mouseX < 475) and (485 <= mouseY < 535): # Return to Menu from Difficulty
            mode = "Menu"
            playsounds(sounds, 4, minim)