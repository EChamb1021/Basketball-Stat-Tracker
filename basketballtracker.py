#Project Title: Basketball Game Stat Tracker
#Name: Evan Chambers
#Username: evan_chambers21
#Date Started: June 1st, 2020
#Date Completed: July 1st, 2020
#Description: 


#Tkinter used for the control panel
from tkinter import *
from tkinter import messagebox
import tkinter.font as font

#Matplotlib used for the live graph
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Styling the plot
plt.style.use('fivethirtyeight')

#The current y value being plotted
global current_y

#The current x value being plotted (time)
global current_time

#Used to animate the graph
global ani

#Adds either 0 seconds or 1 second to the 15 minute timer depending on whether or not thte graph is paused
global time_interval

#Colour of the line
global line_color

#List of X values added to the graph 
global x_values

#List of Y values added to the graph
global y_values

#A tuple (x1,x2) which is graphed every second
#In order to change the colour of the lines depending on the button pressed, 1 second line segments must be used rather than a continuous line
global segment_x_list

#A tuple (y1,y2) is graphed every second by the same logic as above
global segment_y_list

#Boolean which is true when the graph is paused and false when it is running
global graph_paused


#The graph starts in the paused state
graph_paused = True

time_interval = 0.00


x_values = []
y_values = []

segment_x_list = []
segment_y_list = []

current_y = 0
current_time = 0

line_color = 'pink'

#Creating the Tkinter window
window = Tk()

#Window Title
window.title("Control Panel")

#Window Size
window.geometry("440x200")

#Called when the Shot Made button is pressed
def shotMade():

    global current_y
    global line_color

    #a made shot adds 1 to the score and the line turns green
    current_y+=1
    line_color = 'green'

#Called when the Shot Missed button is pressed
def shotMissed():

    global current_y
    global line_color

    #Shot Missed subtracts 1 from the score and the line becomes red
    current_y-=1
    line_color = 'green'

#Called when the Pass button is pressed
def _pass_():

    global current_y
    global line_color

    #Pass adds 0.5 to the score and the line becomes blue
    current_y += 0.5
    line_color = 'blue'

#Called when the Shot Made button is pressed
def turnover():

    global current_y
    global line_color

    #Turnover subtracts 1 from the score and the line turns red
    current_y-=1
    line_color = 'red'
    
#Called when the Shot Made button is pressed
def rebound():

    global current_y
    global line_color

    #Rebound adds 1 to the score and the line turns yellow
    current_y += 1.00
    line_color = 'yellow'

#Called when the play button is pressed
def play_graph():
    global graph_paused
    global time_interval

    #The graph moves at 1 FPS
    time_interval = 1.00

    graph_paused = False

    #Starts the graph animation
    ani.event_source.start()
    
    #Enabling buttons when the graph is in the running state
    shot_made_button['state'] = NORMAL
    shot_missed_button['state'] = NORMAL
    pass_button['state'] = NORMAL
    turnover_button['state'] = NORMAL
    rebound_button['state'] = NORMAL
    pause_button['state'] = NORMAL

    #Disabling buttons when thte graph is in the running state
    reset_button['state'] = DISABLED
    undo_button['state'] = DISABLED
    play_button['state'] = DISABLED
    

#Called when the paused button pressed
def pause_graph():


    global graph_paused
    global time_interval

    #Pauses the graph
    time_interval = 0.00
    ani.event_source.stop()

    graph_paused = True

    #Enabling buttons when the graph is in the running state
    reset_button['state'] = NORMAL
    undo_button['state'] = NORMAL
    play_button['state'] = NORMAL

    #Disabling buttons when thte graph is in the running state
    shot_made_button['state'] = DISABLED
    shot_missed_button['state'] = DISABLED
    pass_button['state'] = DISABLED
    turnover_button['state'] = DISABLED
    rebound_button['state'] = DISABLED
    pause_button['state'] = DISABLED


    
#Called when the new_graph button is pressed
def new_graph():

    global current_time
    global x_values
    global y_values
    global time_interval
    global segment_x_list
    global segment_y_list

    #Resets the graph back to zero and pauses it
    current_time = 0
    time_interval = 0.00

    #Clears the x and y values
    x_values.clear()
    y_values.clear()

    #Clears the segment tuples
    segment_x_list.clear()
    segment_y_list.clear()

    #Clears the Matplotlib plot
    plt.cla()

    #Disabling buttons to match paused state
    shot_made_button['state'] = DISABLED
    shot_missed_button['state'] = DISABLED
    pass_button['state'] = DISABLED
    turnover_button['state'] = DISABLED
    rebound_button['state'] = DISABLED
    undo_button['state'] = DISABLED
    pause_button['state'] = DISABLED

    #Starts the animation
    ani.event_source.start()

#Called when the undo button is pressed
def undo():
    
    global current_time
    global current_y
    global segment_x_list
    global segment_y_list

    #There must be at least one x and one y value for undo to work
    if len(x_values) > 1 and len(y_values) > 1:

        #Removes thet last x and y values
        x_values.pop()
        y_values.pop()

        #Sets the current time to the previous one and the current y to the previous one
        current_time = round(x_values[len(x_values)-1]*60)
        current_y = y_values[len(y_values)-1]

        #Removes the line that was plotted last 
        ax = plt.gca()
        ax.lines.remove(ax.lines[len(ax.lines)-1])

#Called when the wuit button is pressed
def quit_program():

    #Close the control panel and the plot
    window.destroy()
    plt.close()

#CAlled once the 15 minute timer ends
def end_plot():

    #notifies the user that the quarter has ended
    messagebox.showinfo("","15 Minute Quarter Finished.")

    #Disabling all buttons in the control panel except new graph and quit
    shot_made_button['state'] = DISABLED
    shot_missed_button['state'] = DISABLED
    pass_button['state'] = DISABLED
    turnover_button['state'] = DISABLED
    rebound_button['state'] = DISABLED
    undo_button['state'] = DISABLED
    pause_button['state'] = DISABLED
    play_button['state'] = DISABLED

    pause_graph()

#Used to animate the graph
#Runs once every second
def animate(i):

    global current_time
    global line_color
    global segment_x_list
    global segment_y_list
    global time_interval

    #Pauses the graph if pause is pressed
    if graph_paused:
        pause_graph()
    
    #Update the x value in seconds and convert it to minutes
    current_time += time_interval
    minute_current_time = round(current_time/60,3)

    #The animation stops when the timer reaches 15 minutes
    if minute_current_time >= 15.00:
        end_plot()
    
    #Adding the new x and y values to the lists
    x_values.append(minute_current_time)
    y_values.append(current_y)

    #Each segment has points x1 and x2 where x2 is the current time and x1 is the previous time, plotting a line of length 1
    segment_x1 = x_values[len(x_values)-2]
    segment_x2 = minute_current_time

    #Same logic as above for y values
    segment_y1 = y_values[len(y_values)-2]
    segment_y2 = current_y

    #When the graph starts it plots a line of length 0 until the play button is pressed
    if minute_current_time == 0.00:
        segment_x1 = minute_current_time

    #Creating the tuples to be plotted
    segment_x_list = [segment_x1,segment_x2]
    segment_y_list = [segment_y1,segment_y2]

    plt.xlabel("Minutes")
    plt.tight_layout()

    #Plotting the data
    plt.plot(segment_x_list,segment_y_list,color=line_color)

    #Line colour is set back to pink for the neutral state
    line_color = 'pink'


#Creating the buttons for left side of the control panel 
shot_made_button = Button(window,text="SHOT MADE",padx=11,bg="green",command=shotMade)
shot_missed_button = Button(window,text="SHOT MISSED",padx=2,bg="red",command=shotMissed)
rebound_button = Button(window,text="REBOUND",padx=22,bg="yellow",command=rebound)
pass_button = Button(window,text="PASS",padx=44,bg="blue",command=_pass_)
turnover_button = Button(window,text="TURNOVER",bg="red",padx=16,command=turnover)

#Buttons for the right side of the control panel
reset_button = Button(window,text="NEW GRAPH",padx=80,command=new_graph)
play_button = Button(window,text="PLAY",padx=115,command=play_graph)
pause_button = Button(window,text="PAUSE",padx=108,command=pause_graph)
undo_button = Button(window,text="UNDO",padx=111,command=undo)
quit_button = Button(window,text="QUIT",padx=115,command=quit_program)

#Setting the font for the buttons
button_font = font.Font(size=15)

shot_made_button['font'] = button_font
shot_missed_button['font'] = button_font
pass_button['font'] = button_font
turnover_button['font'] = button_font
rebound_button['font'] = button_font
reset_button['font'] = button_font
play_button['font'] = button_font
undo_button['font'] = button_font
pause_button['font'] = button_font
quit_button['font'] = button_font

#The left buttons and the pause and undo buttons are initially disabled until the user clicks play
shot_made_button['state'] = DISABLED
shot_missed_button['state'] = DISABLED
pass_button['state'] = DISABLED
turnover_button['state'] = DISABLED
rebound_button['state'] = DISABLED
undo_button['state'] = DISABLED
pause_button['state'] = DISABLED


#Writing the buttons to the screen
shot_made_button.grid(row=0,column=0)
shot_missed_button.grid(row=1,column=0)
rebound_button.grid(row=2,column=0)
pass_button.grid(row=3,column=0)
turnover_button.grid(row=4,column=0)

reset_button.grid(row=0,column=1)
play_button.grid(row=1,column=1)
pause_button.grid(row=2,column=1)
undo_button.grid(row=3,column=1)
quit_button.grid(row=4,column=1)

#Gets the current plot, calls animate function every 1000ms (1s)
ani = FuncAnimation(plt.gcf(), animate, interval=1000)

#Displays the graph and the control panel
plt.show()
window.mainloop()

