from matplotlib import pyplot as plt
from scipy.interpolate import spline
from scipy.optimize  import curve_fit
import numpy as np
import ast
import csv
from database import Database
from scipy.special import erf

def getx(T,n):
    #settings = {'table name':'t_%dqubit'%n}
    #d = Database(settings,'simlab_db','simlabuser1','db.cs.usask.ca','simlab_01')
    #data = d.get_best_value({'T':T})
    result = np.array([-0.84092,-2.02873,-2.47269,2.05377,-0.637815,-0.68984,1.01427,-0.459972,-0.692359,0.286829,1.07903,0.817047,-0.212273,-0.378047,-1.41365,-0.357701,0.380185,0.127197,0.264516,-0.6539,1.28921,0.0349418,0.701791,0.342238,0.0791158,0.261221,0.0339186,1.0841,-2.09971,1.67246,0.934958,0.881971,0.621297,0.436809,1.29365,-0.354638,1.69556,0.921125,-0.443686,-0.286702,0.270446,1.67924,0.559276,0.461874,-0.964019,0.0942784,1.06151,-2.25931,-0.726677,0.450362,1.47236,-0.141001,0.026939,-0.587468,-0.33656,0.26649,1.67209,0.987759,-0.68186,-2.45212,-0.977972,-0.445514,-0.528124,0.727256,0.79991,0.671903,-0.906704,-0.144535,-0.328303,2.25041,1.29324,0.996094,1.81723,-0.0270453,-0.131744,-2.02845,0.490945,0.123219])

    #x = data['x']


    result = result.reshape(T,n)
    return result

def errorFunctionPlot(T,n):

    result = getx(T,n)

    delta1 = np.array(result[:,0]).ravel()
    delta2 = np.array(result[:,1]).ravel()
    delta3 = np.array(result[:,2]).ravel()

    t1 = np.arange(0.5,T,1.0)
    t = range(0,T-1)
    t2 = np.arange(0,T-1,0.1)
    error1 = []
    error2 = []
    error3 = []

    e_pulse1 = []
    e_pulse2 = []
    e_pulse3 = []

    delta_t = T/(T*3-1)
    for i in  range(0,T-1):
        error1.append( ((delta1[i]+delta1[i+1])/2)+((delta1[i+1]-delta1[i])/2)*erf((4/(t1[i+1]-t1[i]))*(i-((t1[i]+t1[i+1])/2))))
        error2.append( ((delta2[i]+delta2[i+1])/2)+((delta2[i+1]-delta2[i])/2)*erf((4/(t1[i+1]-t1[i]))*(i-((t1[i]+t1[i+1])/2))))
        error3.append( ((delta3[i]+delta3[i+1])/2)+((delta3[i+1]-delta3[i])/2)*erf((4/(t1[i+1]-t1[i]))*(i-((t1[i]+t1[i+1])/2))))

    t2 = np.arange(0.0,T-2,0.1)

    for i in range(0,len(t2)):
        j = int(np.floor(t2[i]))
        e_pulse1.append(((delta1[j]+delta1[j+1])/2)+(((delta1[j+1]-delta1[j])/2)*erf((4/((j+1)-j))*(i-(j+(j+1)))/2)))
        e_pulse2.append(((delta2[j]+delta2[j+1])/2)+((delta2[j+1]-delta2[j])/2)*erf((4/((j+1)-j))*(i-(j+(j+1))/2)))
        e_pulse3.append(((delta3[j]+delta3[j+1])/2)+((delta3[j+1]-delta3[j])/2)*erf((4/((j+1)-j))*(i-(j+(j+1))/2)))


    plt.plot(t2,e_pulse1,label=r'$\epsilon_1$')
    plt.plot(t2,e_pulse2,label=r'$\epsilon_2$')
    plt.plot(t2,e_pulse3,label=r'$\epsilon_3$')

    plt.plot(t,error1,'o',color='black')
    plt.plot(t,error3,'o',color='black')
    plt.plot(t,error2,'o',color='black')


   # plt.legend()

    plt.title("Piecewise error function pulse")
    plt.ylabel(r'$\Delta_{1,2,3}$ (GHz)')
    plt.xlabel(r'$\tau$ (ns)')
    plt.xlim(0,T)
    plt.ylim(-2.5,2.5)

    plt.show()


  #  return omega_off + ((omega_on - omega_off)/2)(erf((4*t-2*t_ramp)/t_ramp)-erf((4*t-4*t_gate+2*t_ramp)/t_ramp))

def piecewiseConstantPlot(T,n):

    result = getx(T,n)

    delta1 = np.array(result[:,0]).ravel()
    delta2 = np.array(result[:,1]).ravel()
    delta3 = np.array(result[:,2]).ravel()

    t = np.arange(0.0,T,0.1)
    t1 = np.arange(0.5,T,1.0)

    pulse1 = [];
    pulse2 = [];
    pulse3 = [];


    for i in range(0,len(t)):
        j = int(np.floor(t[i]))
        pulse1.append(delta1[j])
        pulse2.append(delta2[j])
        pulse3.append(delta3[j])


    plt.plot(t,pulse1,label=r'$\Delta_1$')
    plt.plot(t,pulse2,label=r'$\Delta_2$')
    plt.plot(t,pulse3,label=r'$\Delta_3$')

    plt.plot(t1,delta1,'o',color='black')
    plt.plot(t1,delta3,'o',color='black')
    plt.plot(t1,delta2,'o',color='black')


    plt.legend()

    plt.title("Piecewise constant pulse")
    plt.ylabel(r'$\Delta_{1,2,3}$ (GHz)')
    plt.xlabel(r'$\tau$ (ns)')
    plt.xlim(0,T)
    plt.ylim(-2.5,2.5)

    plt.savefig('T_%d_pc.png'%T)

if __name__ == '__main__':
       # piecewiseConstantPlot(26,3)
        errorFunctionPlot(26,3)



