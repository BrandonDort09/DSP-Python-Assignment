import numpy as np
import matplotlib.pyplot as plt


def highpassDesign(sampling_rate,cutoff_frequencies,Frequency_Resolution):
    fs = sampling_rate
    M = int(fs/Frequency_Resolution)
    k = int(cutoff_frequencies/fs *M)
    X = np.ones(M)
    X[0:k] = 0
    X[M - k:M - 1] = 0

    X = np.hamming(M)

    return X




def bandstopDesign(sampling_rate,cutoff_frequencies,Frequency_Resolution):
        fs = sampling_rate
        M = int(fs / Frequency_Resolution)
        k1 = int(cutoff_frequencies[0]/fs * M)
        k2 = int(cutoff_frequencies[1] / fs * M)
        X = np.ones(M)
        X[k1:k2+1] = 0
        X[M-k2:M-k1+1] = 0
        X = np.real(X)
        X = np.hamming(M)

        return X


def ifft(coefficients):
    x = np.fft.ifft(coefficients)
    x = np.real(x)

    return x

def createWavelet():
    a = 1
    A = 2/(np.sqrt(3*a)*(np.pi**0.25))
    x = np.arange(-32,32,0.32)
    y = 0.0007*A*(1-(x/a)**2)*np.exp(-0.5*(x/a)**2)
    plt.plot(y)
    plt.show()

    return y


class FIRfilter:
    def __init__(self,_coefficients,Frequency_Resolution = 1):
        self.ntaps = len(_coefficients)  # ntaps is the number of coefficients
        self.coefficients = _coefficients  # define the variable called coefficients to save the coeffient of FIR
        self.buffer = np.zeros(self.ntaps)  # buffer is used to save the input value
        self.Frequency_Resolution = Frequency_Resolution
    def dofilter(self,v):
        for j in range(self.ntaps - 1):
            self.buffer[self.ntaps - 1 - j] = self.buffer[self.ntaps - 2 - j]  # as time goes by move the past value x(n) to x(n-1)
        self.buffer[0] = v  # assign the v to buffer[0] as the current input value

        return np.inner(self.buffer, self.coefficients)

if __name__ == '__main__':
    y1 = createWavelet()
    data = np.loadtxt('ECG_ugrad_matric_9.dat')
    # data_max = np.min(data)
    # data = data/data_max
    # plt.plot(data)
    # plt.show()
    Frequency_Resolution = 1
    OutputAfterHighpassFilter = np.zeros(len(data))
    OutputAfterBandStopFilter = np.zeros(len(data))
    res = np.zeros(len(data))

    # create bandstop filter
    cutoff_frequencies1 = [45, 55]
    coefficients1 = bandstopDesign(250, cutoff_frequencies1, Frequency_Resolution)
    x = ifft(coefficients1)
    filter1 = FIRfilter(x)

    #create high pass filter
    cutoff_frequencies2 = 5
    coefficients2 = highpassDesign(250, cutoff_frequencies2, Frequency_Resolution)
    x = ifft(coefficients2)
    filter2 = FIRfilter(x)

    #Processing of eliminating baseline wander
    for i in range(len(data)):
        OutputAfterHighpassFilter[i]= filter1.dofilter(data[i])

    for i in range(len(data)):
        OutputAfterBandStopFilter[i] = filter2.dofilter(OutputAfterHighpassFilter[i])

    # template =  OutputAfterBandStopFilter[400:600]  # create template
    # plt.plot(template)
    # plt.show()
    template = createWavelet()
    fir_coeff = template[::-1]  # reverse time
    filter = FIRfilter(fir_coeff)

    for i in range(len(data)):
        res[i] = filter.dofilter(OutputAfterBandStopFilter[i])

        res[i] = res[i] * res[i]

    plt.plot(res)
    plt.show()
