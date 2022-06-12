import tkinter as tk

import Header
import DiagramComponents


class Liquid_Engine_Plumbing:

    def __init__(self, gridLen):

        width = gridLen * 8
        height = gridLen * 12

        self.win = tk.Tk()
        self.win.title("P&ID Diagram")
        self.win.geometry(str(width) + "x" + str(height))
        self.win.configure(bg='black')

        # CONSTANT
        fluidColor = '#41d94d'

        # HEADER
        self.header = Header.Header(self.win, 'black', 'P&ID', width, gridLen, 24)
        self.header.getWidget().place(x=gridLen * 0, y=gridLen * 0)

        # All TANKS
        self.gn2 = DiagramComponents.Tank(self.win, 'black', 'GN2', '#1d2396', gridLen, gridLen)
        self.lox = DiagramComponents.Tank(self.win, 'black', 'LOx', '#1d2396', gridLen, gridLen)
        self.k = DiagramComponents.Tank(self.win, 'black', 'K', '#1d2396', gridLen, gridLen)
        self.gn2.getWidget().place(x=gridLen * 3, y=gridLen * 1)
        self.lox.getWidget().place(x=gridLen * 1, y=gridLen * 5)
        self.k.getWidget().place(x=gridLen * 6, y=gridLen * 5)

        # All SOLENOID VALVES
        self.one = DiagramComponents.Solenoid(self.win, 'black', 1, gridLen, gridLen, False, True, True, False)
        self.two = DiagramComponents.Solenoid(self.win, 'black', 2, gridLen, gridLen, False, True, False, False)
        self.three = DiagramComponents.Solenoid(self.win, 'black', 3, gridLen, gridLen, False, False, True, True)
        self.four = DiagramComponents.Solenoid(self.win, 'black', 4, gridLen, gridLen, False, True, False, False)
        self.five = DiagramComponents.Solenoid(self.win, 'black', 5, gridLen, gridLen, True, False, False, True)
        self.six = DiagramComponents.Solenoid(self.win, 'black', 6, gridLen, gridLen, False, True, False, True)
        self.one.getWidget().place(x=gridLen * 1, y=gridLen * 2)
        self.one.setIn(2)
        self.one.setOut(3)
        self.two.getWidget().place(x=gridLen * 0, y=gridLen * 4)
        self.two.setIn(2)
        self.three.getWidget().place(x=gridLen * 6, y=gridLen * 2)
        self.three.setIn(4)
        self.three.setOut(3)
        self.four.getWidget().place(x=gridLen * 5, y=gridLen * 4)
        self.four.setIn(2)
        self.five.getWidget().place(x=gridLen * 3, y=gridLen * 8)
        self.five.setIn(1)
        self.five.setOut(4)
        self.six.getWidget().place(x=gridLen * 4, y=gridLen * 7)
        self.six.setIn(4)
        self.six.setOut(2)

        # All STEPPER
        self.s1 = DiagramComponents.Stepper(self.win, 'black', gridLen, gridLen, True, False, False, True)
        self.s2 = DiagramComponents.Stepper(self.win, 'black', gridLen, gridLen, False, True, True, True)
        self.s1.getWidget().place(x=gridLen * 6, y=gridLen * 7)
        self.s2.getWidget().place(x=gridLen * 2, y=gridLen * 8)

        # All ORIFICES
        self.o1 = DiagramComponents.Orifice(self.win, 'black', gridLen, gridLen, True, False, True, False)
        self.o2 = DiagramComponents.Orifice(self.win, 'black', gridLen, gridLen, False, True, True, True)
        self.o1.getWidget().place(x=gridLen * 1, y=gridLen * 6)
        self.o2.getWidget().place(x=gridLen * 5, y=gridLen * 7)

        # All Pressure Sensors
        self.ps1 = DiagramComponents.PressureSensor(self.win, 'black', gridLen, gridLen, False, True, False, False)
        self.ps2 = DiagramComponents.PressureSensor(self.win, 'black', gridLen, gridLen, False, False, False, True)
        self.ps3 = DiagramComponents.PressureSensor(self.win, 'black', gridLen, gridLen, False, True, True, True)
        self.ps1.getWidget().place(x=gridLen * 0, y=gridLen * 3)
        self.ps2.getWidget().place(x=gridLen * 7, y=gridLen * 3)
        self.ps3.getWidget().place(x=gridLen * 5, y=gridLen * 9)

        self.tp1 = DiagramComponents.TempSensor(self.win, 'black', gridLen, gridLen, True, False, False, False)
        self.tp1.getWidget().place(x=gridLen * 5, y=gridLen * 10)

        # All Text boxes
        self.t1 = Header.Text(self.win, 'black', 'K Fill', gridLen, gridLen, 12)
        self.t2 = Header.Text(self.win, 'black', 'K Drain', gridLen, gridLen, 12)
        self.t3 = Header.Text(self.win, 'black', 'LOx\nFill/Drain', gridLen, gridLen, 12)
        self.t4 = Header.Text(self.win, 'black', 'Regen\nCircuit', gridLen, gridLen, 12)
        self.t1.getWidget().place(x=gridLen * 7, y=gridLen * 4)
        self.t2.getWidget().place(x=gridLen * 7, y=gridLen * 6)
        self.t3.getWidget().place(x=gridLen * 1, y=gridLen * 9)
        self.t4.getWidget().place(x=gridLen * 7, y=gridLen * 9)

        # All PIPES
        self.p1 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, False, True, False, True, '#41d94d', False)
        self.p2 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, True, '#41d94d', False)
        self.p3 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, False, True, False, True, '#41d94d', False)
        self.p4 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, False, True, False, True, '#41d94d', False)
        self.p5 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, True, '#41d94d', False)
        self.p6 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p7 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, False, '#41d94d', False)
        self.p8 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, True, '#41d94d', False)
        self.p9 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p10 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, True, '#41d94d', False)
        self.p11 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p12 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p13 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, False, '#41d94d', False)
        self.p14 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, True, False, '#41d94d', False)
        self.p15 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, False, '#41d94d', False)
        self.p16 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, False, '#41d94d', False)
        self.p17 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, False, False, '#41d94d', False)
        self.p18 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, False, False, True, True, '#41d94d', False)
        self.p19 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, False, False, '#41d94d', False)
        self.p20 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, False, True, True, True, '#41d94d', False)
        self.p21 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, False, True, False, True, '#41d94d', False)
        self.p22 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, False, True, '#41d94d', False)
        self.p1.getWidget().place(x=gridLen * 2, y=gridLen * 2)
        self.p2.getWidget().place(x=gridLen * 3, y=gridLen * 2)
        self.p3.getWidget().place(x=gridLen * 4, y=gridLen * 2)
        self.p4.getWidget().place(x=gridLen * 5, y=gridLen * 2)
        self.p5.getWidget().place(x=gridLen * 1, y=gridLen * 3)
        self.p6.getWidget().place(x=gridLen * 3, y=gridLen * 3)
        self.p7.getWidget().place(x=gridLen * 6, y=gridLen * 3)
        self.p8.getWidget().place(x=gridLen * 1, y=gridLen * 4)
        self.p9.getWidget().place(x=gridLen * 3, y=gridLen * 4)
        self.p10.getWidget().place(x=gridLen * 6, y=gridLen * 4)
        self.p11.getWidget().place(x=gridLen * 3, y=gridLen * 5)
        self.p12.getWidget().place(x=gridLen * 3, y=gridLen * 6)
        self.p13.getWidget().place(x=gridLen * 6, y=gridLen * 6)
        self.p14.getWidget().place(x=gridLen * 1, y=gridLen * 7)
        self.p15.getWidget().place(x=gridLen * 3, y=gridLen * 7)
        self.p16.getWidget().place(x=gridLen * 1, y=gridLen * 8)
        self.p17.getWidget().place(x=gridLen * 5, y=gridLen * 8)
        self.p18.getWidget().place(x=gridLen * 6, y=gridLen * 8)
        self.p19.getWidget().place(x=gridLen * 2, y=gridLen * 9)
        self.p20.getWidget().place(x=gridLen * 3, y=gridLen * 9)
        self.p21.getWidget().place(x=gridLen * 4, y=gridLen * 9)
        self.p22.getWidget().place(x=gridLen * 6, y=gridLen * 9)

        # NOZZLE
        self.n = DiagramComponents.Nozzle(self.win, 'black', gridLen, gridLen * 1.5)
        self.n.getWidget().place(x=gridLen * 3, y=gridLen * 10)

        #self.s2.setNeighbors(None, self.five, self.p19, self.p16)
        #self.s1.setNeighbors(self.p13, None, None, self.o2)


        #SET ALL VIRTUAL COMPONENTS (linked list)
        self.head = self.gn2
        #row 1
        self.gn2.setNeighbors(None, None, self.p2, None)
        #row 2
        self.one.setNeighbors(None, None, self.p5, None)
        self.p1.setNeighbors(None, None, None, self.one)
        self.p2.setNeighbors(None, self.p3, self.p6, self.p1)
        self.p3.setNeighbors(None, self.p4, None, None)
        self.p4.setNeighbors(None, self.three, None, None)
        self.three.setNeighbors(None, None, self.p7, None)
        #row 3
        self.ps1.setNeighbors(None, None, None, None)
        self.p5.setNeighbors(None, None, self.p8, self.ps1)
        self.p6.setNeighbors(None, None, self.p9, None)
        self.p7.setNeighbors(None, self.ps2, self.p10, None)
        self.ps2.setNeighbors(None, None, None, None)
        #row 4
        self.two.setNeighbors(None, None, None, None)
        self.p8.setNeighbors(None, None, self.lox, self.two)
        self.p9.setNeighbors(None, None, self.p11, None)
        self.four.setNeighbors(None, None, None, None)
        self.p10.setNeighbors(None, None, self.k, self.four)
        #row5
        self.lox.setNeighbors(None, None, self.o1, None)
        self.p11.setNeighbors(None, None, self.p12, None)
        self.k.setNeighbors(None, None, self.p13, None)
        #row 6
        self.o1.setNeighbors(None, None, self.p14, None)
        self.p12.setNeighbors(None, None, self.p15, None)
        self.p13.setNeighbors(None, None, self.s1, None)
        #row 7
        self.p14.setNeighbors(None, None, self.p16, None)
        self.p15.setNeighbors(None, self.six, self.five, None)
        self.six.setNeighbors(None, self.o2, None, None)
        self.o2.setNeighbors(None, None, self.p17, None)
        self.s1.setNeighbors(None, None, None, self.o2)
        #row 8
        self.p16.setNeighbors(None, self.s2, None, None)
        self.s2.setNeighbors(None, None, self.p19, None)
        self.five.setNeighbors(None, None, None, self.s2)
        self.p17.setNeighbors(None, self.p18, None, None)
        self.p18.setNeighbors(None, None, self.p22, None)
        #row 9
        self.p19.setNeighbors(None, self.p20, None, None)
        self.p20.setNeighbors(None, None, self.n, None)
        self.p21.setNeighbors(None, None, None, self.p20)
        self.ps3.setNeighbors(None, None, self.tp1, self.p21)
        self.p22.setNeighbors(None, None, None, self.ps3)
        #row 10
        self.n.setNeighbors(None, None, None, None)
        self.tp1.setNeighbors(None, None, None, None)

        """# SET ALL VIRTUAL COMPONENTS (doubly linked list)
        self.head = self.gn2
        # row 1
        self.gn2.setNeighbors(None, None, self.p2, None)
        # row 2
        self.one.setNeighbors(None, self.p1, self.p5, None)
        self.p1.setNeighbors(None, self.p2, None, self.one)
        self.p2.setNeighbors(self.gn2, self.p3, self.p6, self.p1)
        self.p3.setNeighbors(None, self.p4, None, self.p2)
        self.p4.setNeighbors(None, self.three, None, self.p3)
        self.three.setNeighbors(None, None, self.p7, self.p4)
        # row 3
        self.ps1.setNeighbors(None, self.p5, None, None)
        self.p5.setNeighbors(self.one, None, self.p8, self.ps1)
        self.p6.setNeighbors(self.p2, None, self.p9, None)
        self.p7.setNeighbors(self.three, self.ps2, self.p10, None)
        self.ps2.setNeighbors(None, None, None, self.p7)
        # row 4
        self.two.setNeighbors(None, self.p8, None, None)
        self.p8.setNeighbors(self.p5, None, self.lox, self.two)
        self.p9.setNeighbors(self.p6, None, self.p11, None)
        self.four.setNeighbors(None, self.p10, None, None)
        self.p10.setNeighbors(self.p7, None, self.k, self.four)
        # row5
        self.lox.setNeighbors(self.p8, None, self.o1, None)
        self.p11.setNeighbors(self.p9, None, self.p12, None)
        self.k.setNeighbors(self.p10, None, self.p13, None)
        # row 6
        self.o1.setNeighbors(self.lox, None, self.p14, None)
        self.p12.setNeighbors(self.p11, None, self.p15, None)
        self.p13.setNeighbors(self.k, None, self.s1, None)
        # row 7
        self.p14.setNeighbors(self.o1, None, self.p16, None)
        self.p15.setNeighbors(self.p12, self.six, self.five, None)
        self.six.setNeighbors(None, self.o2, None, self.p15)
        self.o2.setNeighbors(None, self.s1, self.p17, self.six)
        self.s1.setNeighbors(self.p13, None, None, self.o2)
        # row 8
        self.p16.setNeighbors(self.p14, self.s2, None, None)
        self.s2.setNeighbors(None, self.five, self.p19, self.p16)
        self.five.setNeighbors(self.p15, None, None, self.s2)
        self.p17.setNeighbors(self.o2, self.p18, None, None)
        self.p18.setNeighbors(None, None, self.p22, self.p17)
        # row 9
        self.p19.setNeighbors(self.s2, self.p20, None, None)
        self.p20.setNeighbors(None, self.p21, self.n, self.p19)
        self.p21.setNeighbors(None, self.ps3, None, self.p20)
        self.ps3.setNeighbors(None, self.p22, self.tp1, self.p21)
        self.p22.setNeighbors(self.p18, None, None, self.ps3)
        # row 10
        self.n.setNeighbors(self.p20, None, None, None)
        self.tp1.setNeighbors(self.ps3, None, None, None)"""

    def defaultState(self):
        self.p1.setState(False)
        self.p2.setState(False)
        self.p3.setState(False)
        self.p4.setState(False)
        self.p5.setState(False)
        self.p6.setState(False)
        self.p7.setState(False)
        self.p8.setState(False)
        self.p9.setState(False)
        self.p10.setState(False)
        self.p11.setState(False)
        self.p12.setState(False)
        self.p13.setState(False)
        self.p14.setState(False)
        self.p15.setState(False)
        self.p16.setState(False)
        self.p17.setState(False)
        self.p18.setState(False)
        self.p19.setState(False)
        self.p20.setState(False)
        self.p21.setState(False)
        self.p22.setState(False)

        self.one.setPipes(False, False, False, False)
        self.two.setPipes(False, False, False, False)
        self.three.setPipes(False, False, False, False)
        self.four.setPipes(False, False, False, False)
        self.five.setPipes(False, False, False, False)
        self.six.setPipes(False, False, False, False)

        self.ps1.setPipes(False)
        self.ps2.setPipes(False)
        self.ps3.setPipes(False)

        self.o1.setPipes(False)
        self.o2.setPipes(False)

        self.s1.setPipes(False, False, False, False)
        self.s2.setPipes(False, False, False, False)

        self.tp1.setPipes(False)



    def getHead(self):
        return self.gn2

    def updatePipeStatus(self):
        self.defaultState()

        head = self.getHead()

        listMultiplePaths = []
        visited = []
        listMultiplePaths.append(head)

        # Basic traversal method
        while(len(listMultiplePaths) > 0):
            if(type(head) is DiagramComponents.Pipe):
                head.setState(True)

            if (head.top is not None and head.top not in visited):
                if(type(head.top) is DiagramComponents.Solenoid and head.top.getState()):
                    listMultiplePaths.append(head.top)
                    visited.append(head.top)
                elif(type(head.top) is not DiagramComponents.Solenoid and type(head.top) is not DiagramComponents.Stepper):
                    listMultiplePaths.append(head.top)
                    visited.append(head.top)
                elif (type(head.top) is DiagramComponents.Stepper and head.top.getPercentage() > 0):
                    listMultiplePaths.append(head.top)
                    visited.append(head.top)
            if (head.right is not None and head.right not in visited):
                if (type(head.right) is DiagramComponents.Solenoid and head.right.getState()):
                    listMultiplePaths.append(head.right)
                    visited.append(head.right)
                elif (type(head.right) is not DiagramComponents.Solenoid and type(head.right) is not DiagramComponents.Stepper):
                    listMultiplePaths.append(head.right)
                    visited.append(head.right)
                elif (type(head.right) is DiagramComponents.Stepper and head.right.getPercentage() > 0):
                    listMultiplePaths.append(head.right)
                    visited.append(head.right)
            if (head.bottom is not None and head.bottom not in visited):
                if (type(head.bottom) is DiagramComponents.Solenoid and head.bottom.getState()):
                    listMultiplePaths.append(head.bottom)
                    visited.append(head.bottom)
                elif (type(head.bottom) is not DiagramComponents.Solenoid and type(head.bottom) is not DiagramComponents.Stepper):
                    listMultiplePaths.append(head.bottom)
                    visited.append(head.bottom)
                elif (type(head.bottom) is DiagramComponents.Stepper and head.bottom.getPercentage() > 0):
                    listMultiplePaths.append(head.bottom)
                    visited.append(head.bottom)
            if (head.left is not None and head.left not in visited):
                if (type(head.left) is DiagramComponents.Solenoid and head.left.getState()):
                    listMultiplePaths.append(head.left)
                    visited.append(head.left)
                elif (type(head.left) is not DiagramComponents.Solenoid and type(head.left) is not DiagramComponents.Stepper):
                    listMultiplePaths.append(head.left)
                    visited.append(head.left)
                elif (type(head.left) is DiagramComponents.Stepper and head.left.getPercentage() > 0):
                    listMultiplePaths.append(head.left)
                    visited.append(head.left)

            listMultiplePaths.pop(0)
            if(len(listMultiplePaths) > 0):
                head = listMultiplePaths[0]
            else:
                break

        #edge checks for components with pipes (excluding pipes)
        if(self.p1.getState()):
            self.one.setFill(False, True, False, False)
        if(self.p4.getState()):
            self.three.setFill(False, False, False, True)
        if(self.p5.getState()):
            self.one.setFill(False, False, True, False)
            self.ps1.setFill(False, True, False, False)
        if(self.p7.getState()):
            self.three.setFill(False, False, True, False)
            self.ps2.setFill(False, False, False, True)
        if(self.p8.getState()):
            self.two.setFill(False, True, False, False)
            self.o1.setFill(True, False, False, False)
        if(self.p10.getState()):
            self.four.setFill(False, True, False, False)
        if(self.p14.getState()):
            self.o1.setFill(False, False, True, False)
        if(self.p15.getState()):
            self.five.setFill(True, False, False, False)
            self.six.setFill(False, False, False, True)
            if(self.six.getState()):
                self.six.setFill(False, True, False, False)
                self.o2.setFill(False, False, True, True)
            if(self.five.getState()):
                self.five.setFill(False, False, False, True)
                self.s2.setFill(False, True, False, False)
                if(self.s2.getPercentage() > 0):
                    self.s2.setFill(False, False, True, False)
        if(self.p13.getState()):
            self.s1.setFill(True, False, False, False)
            if(self.s1.getPercentage() > 0):
                self.s1.setFill(False, False, False, True)
                self.o2.setFill(False, True, True, False)
        if(self.p16.getState()):
            self.s2.setFill(False, False, False, True)
            if(self.s2.getPercentage() > 0):
                self.s2.setFill(False, False, True, False)
        if(self.p22.getState()):
            self.ps3.setFill(False, True, True, True)
            self.tp1.setFill(True, False, False, False)

    def getWindow(self):
        return self.win


class Solids_Engine_Plumbing:

    def __init__(self, gridLen):

        width = gridLen * 3
        height = gridLen * 7

        self.win = tk.Tk()
        self.win.title("P&ID Diagram")
        self.win.geometry(str(width) + "x" + str(height))
        self.win.configure(bg='black')

        # CONSTANT
        fluidColor = '#41d94d'

        # HEADER
        self.header = Header.Header(self.win, 'black', 'P&ID', width, gridLen, 24)
        self.header.getWidget().place(x=gridLen * 0, y=gridLen * 0)

        # All TANKS
        self.gn2 = DiagramComponents.Tank(self.win, 'black', 'GN2', '#1d2396', gridLen, gridLen)
        self.ovp = DiagramComponents.Tank(self.win, 'black', 'Over\nPres', '#f542b9', gridLen, gridLen)
        self.gn2.getWidget().place(x=gridLen * 0, y=gridLen * 1)
        self.ovp.getWidget().place(x=gridLen * 2, y=gridLen * 1)

        # All SOLENOID VALVES
        self.one = DiagramComponents.Solenoid(self.win, 'black', 1, gridLen, gridLen, True, False, True, False)
        self.two = DiagramComponents.Solenoid(self.win, 'black', 1, gridLen, gridLen, True, False, True, False)
        self.one.getWidget().place(x=gridLen * 0, y=gridLen * 2)
        self.two.getWidget().place(x=gridLen * 2, y=gridLen * 2)

        # All Pressure Sensors
        self.ps1 = DiagramComponents.PressureSensor(self.win, 'black', gridLen, gridLen, False, False, False, True)
        self.ps1.getWidget().place(x=gridLen * 2, y=gridLen * 4)

        # All Text boxes
        self.t1 = Header.Text(self.win, 'black', 'Relief Valve', gridLen, gridLen, 12)
        self.t2 = Header.Text(self.win, 'black', 'WIRE 1', gridLen, gridLen, 12)
        self.t3 = Header.Text(self.win, 'black', 'WIRE 2', gridLen, gridLen, 12)
        self.t1.getWidget().place(x=gridLen * 0, y=gridLen * 4)
        self.t2.getWidget().place(x=gridLen * 2, y=gridLen * 5)
        self.t3.getWidget().place(x=gridLen * 2, y=gridLen * 6)

        # All PIPES
        self.p1 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, False, False, '#41d94d', False)
        self.p2 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, False, True, True, True, '#41d94d', False)
        self.p3 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, False, False, True, '#41d94d', False)
        self.p4 = DiagramComponents.Pipe(self.win, 'black', gridLen, gridLen, True, True, True, True, '#41d94d', False)
        self.p1.getWidget().place(x=gridLen * 0, y=gridLen * 3)
        self.p2.getWidget().place(x=gridLen * 1, y=gridLen * 3)
        self.p3.getWidget().place(x=gridLen * 2, y=gridLen * 3)
        self.p4.getWidget().place(x=gridLen * 1, y=gridLen * 4)


        # NOZZLE
        self.n = DiagramComponents.Nozzle(self.win, 'black', gridLen, gridLen * 1.5)
        self.n.getWidget().place(x=gridLen * 1, y=gridLen * 5)



    def getWindow(self):
        return self.win