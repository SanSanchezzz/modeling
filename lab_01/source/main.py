from math import *

def setValuesX(begin, end, h):
    valuesX = []
    currentValue = begin

    while (currentValue <= end):
        valuesX.append(currentValue)
        currentValue += h

    return valuesX

def printResult(valuesX, resultP, resultE, resultNE, step):

    for i in range(0, len(valuesX), step):
        if (i < len(resultNE)):
            print('{:^10.5} | {:^15.8f} | {:^15.8f} | {:^15.8f} | {:^15.8f}'.format(valuesX[i], resultP[i][0], resultP[i][1], resultE[i], resultNE[i]))
        elif (i < len(resultE)):
            print('{:^10.5} | {:^15.8f} | {:^15.8f} | {:^15} | {:^15.8f}'.format(valuesX[i], resultP[i][0], resultP[i][1], '-', resultNE[i]))
        else:
            print('{:^10.5} | {:^15.8f} | {:^15.8f} | {:^15} | {:^15}'.format(valuesX[i], resultP[i][0], resultP[i][1], '-', '-'))

def methodPicara(valuesX, y_0):
    def y_1(x):
        return pow(x, 3) / 3.0

    def y_2(x):
        return y_1(x) + pow(x, 7) / 63.0

    def y_3(x):
        return  y_2(x) + 2 * pow(x, 11) / 2079.0 + pow(x, 15) / 59535.0

    def y_4(x):
        return y_3(x) + 2 * pow(x, 15) / 93555.0 + 82 * pow(x, 19) / 37328445.0 + 662 * pow(x, 23) / 10438212015.0 + \
                4 * pow(x, 27) / 3341878155.0 + pow(x, 31) / 109876902975.0

    result = [[y_0, y_0]]

    for i in range(1, len(valuesX)):
        result.append([y_3(valuesX[i]), y_4(valuesX[i])])

    return result

def methodEulerExplicit(valuesX, step, y):
    result = []

    for i in range(len(valuesX)):
        if (y == float('inf')):
            break
        y += step * (y * y + valuesX[i] * valuesX[i])
        result.append(y)

    return result
# def methodEulerExplicit(valuesX, step, y):
    # # def EulerIter()
    # result = []
    # x0 = step
    # f = 0
    # for i in range(len(valuesX)):
        # while (x0 < valuesX[i] + step / 2):
            # f += step * (x0 * x0 + f * f)
            # x0 += step
        # # y += step * (y * y + valuesX[i] * valuesX[i])
        # result.append(f)

    # return result


def methodEulerNExplicit(valuesX, step, y):
    result = []

    for i in range(len(valuesX)):
        discr = 1 - step * 4 * (y + step * (valuesX[i] * valuesX[i]))

        if (discr < 0):
            break

        y = (1 - sqrt(discr)) / (2 * step)
        result.append(y)

    return result

def main():
    y_0 = 0
    beginX = 0.0
    endX = 2.0
    step = 0.0000001
    step_print = 1000000

    X = setValuesX(beginX, endX, step)

    resultPicara = methodPicara(X, y_0)
    resultExplicit = methodEulerExplicit(X, step, y_0)
    resultNExplicit = methodEulerNExplicit(X, step, y_0)

    printResult(X, resultPicara, resultExplicit, resultNExplicit, step_print)

if __name__ == '__main__':
    main()
