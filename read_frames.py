from pgl import GWindow, GCompound, GState, GRect
import random

def read(f):
    done = False
    frames = []
    while not done:
        #print("reading frame")
        poss = []
        #print("new line")
        t = f.readline()
        if t != "":
            array = t.split("/")
            #print(len(array))
            #print(len(array))
            #print(line[0])
            for e in array:
                if e != "":
                    cord = e.split(',')
                    x = float(cord[0])
                    y = float(cord[1])
                    poss.append((x,y))
            #print(len(poss))
            frames.append(poss)
        else:
            done = True
        
    f.close()
    return frames
        

            

def render():
    frames = None
    try:
        name = input("input a file name: ")
        with open(f"examples/{name}","r") as f:
            print("reading frames")
            frames = read(f)
            print("read frames")
            gw = GWindow(800,800)
            gs = GState()
            gs.i = 0
            gs.last = GCompound()
            bg = GRect(800,800)
            bg.set_filled(True)
            gw.add(bg)
            gw.add(gs.last)
            #print(len(frames))
            #print(len(frames[0]))

            colors = ["Skyblue", "Skyblue", "Skyblue", "White", "Blue"]

            def run():

                gw.remove(gs.last)
                gs.last = GCompound()
                frame = frames[gs.i%len(frames)]
                
                scale = 12000
                shiftx = 400#+(gs.i//2)%10000
                shifty = 600#-300+gs.i%10000

                for pos in frame:
                    p = GRect(pos[0]/scale + shiftx,pos[1]/scale + shifty,1,1)
                    p.set_color(colors[random.randrange(0,4)])
                    gs.last.add(p)
                gw.add(gs.last)

                gs.i += 1

            gw.set_interval(run,1)
    except:
        print('that file does not exist')

if __name__ == "__main__":
    #read(open("frames/frames.txt","r"))
    render()