# --------------------------------------------------------------------------
# ------------  Metody Systemowe i Decyzyjne w Informatyce  ----------------
# --------------------------------------------------------------------------
#  Zadanie 1: Regresja liniowa
#  autorzy: A. Gonczarek, J. Kaczmar, S. Zareba
#  2017
# --------------------------------------------------------------------------

import numpy as np
from utils import polynomial


def mean_squared_error(x, y, w):
    '''
    :param x: ciag wejsciowy Nx1
    :param y: ciag wyjsciowy Nx1
    :param w: parametry modelu (M+1)x1
    :return: blad sredniokwadratowy pomiedzy wyjsciami y oraz wyjsciami uzyskanymi z wielowamiu o parametrach w dla wejsc x
    '''
    wx = polynomial(x, w)
    ndArrayOfErr = ((y - wx) ** 2)
    return np.sum(ndArrayOfErr) / y.shape[0]


def design_matrix(x_train, M):
    '''
    :param x_train: ciag treningowy Nx1
    :param M: stopien wielomianu 0,1,2,...
    :return: funkcja wylicza Design Matrix Nx(M+1) dla wielomianu rzedu M
    '''
    designMatrix = np.ones((x_train.shape[0], 1))
    for i in range(1, M + 1):
        designMatrix = np.concatenate([designMatrix, x_train ** i], 1)
    return designMatrix


def least_squares(x_train, y_train, M):
    '''
    :param x_train: ciag treningowy wejscia Nx1
    :param y_train: ciag treningowy wyjscia Nx1
    :param M: rzad wielomianu
    :return: funkcja zwraca krotke (w,err), gdzie w sa parametrami dopasowanego wielomianu, a err blad sredniokwadratowy
    dopasowania
    '''
    designMatrix = design_matrix(x_train, M)
    w = np.linalg.inv(designMatrix.transpose() @ designMatrix) @ designMatrix.transpose() @ y_train
    err = mean_squared_error(x_train, y_train, w)
    return w, err


def regularized_least_squares(x_train, y_train, M, regularization_lambda):
    '''
    :param x_train: ciag treningowy wejscia Nx1
    :param y_train: ciag treningowy wyjscia Nx1
    :param M: rzad wielomianu
    :param regularization_lambda: parametr regularyzacji
    :return: funkcja zwraca krotke (w,err), gdzie w sa parametrami dopasowanego wielomianu zgodnie z kryterium z regularyzacja l2,
    a err blad sredniokwadratowy dopasowania
    '''
    designMatrix = design_matrix(x_train, M)
    unitMatrix = np.eye(designMatrix.shape[1])
    w = np.linalg.inv(designMatrix.T @ designMatrix + regularization_lambda * unitMatrix) \
        @ designMatrix.T @ y_train
    err = mean_squared_error(x_train, y_train, w)
    return w, err


def model_selection(x_train, y_train, x_val, y_val, M_values):
    '''
    :param x_train: ciag treningowy wejscia Nx1
    :param y_train: ciag treningowy wyjscia Nx1
    :param x_val: ciag walidacyjny wejscia Nx1
    :param y_val: ciag walidacyjny wyjscia Nx1
    :param M_values: tablica stopni wielomianu, ktore maja byc sprawdzone
    :return: funkcja zwraca krotke (w,train_err,val_err), gdzie w sa parametrami modelu, ktory najlepiej generalizuje dane,
    tj. daje najmniejszy blad na ciagu walidacyjnym, train_err i val_err to bledy na sredniokwadratowe na ciagach treningowym
    i walidacyjnym
    '''

    bestResult = []
    for m in M_values:
        w, train_err = least_squares(x_train, y_train, m)
        val_err = mean_squared_error(x_val, y_val, w)
        if len(bestResult) < 3 or bestResult[2] > val_err:
            bestResult = w, train_err, val_err
    return bestResult

def regularized_model_selection(x_train, y_train, x_val, y_val, M, lambda_values):
    '''
    :param x_train: ciag treningowy wejscia Nx1
    :param y_train: ciag treningowy wyjscia Nx1
    :param x_val: ciag walidacyjny wejscia Nx1
    :param y_val: ciag walidacyjny wyjscia Nx1
    :param M: stopien wielomianu
    :param lambda_values: lista ze wartosciami roznych parametrow regularyzacji
    :return: funkcja zwraca krotke (w,train_err,val_err,regularization_lambda), gdzie w sa parametrami modelu, ktory najlepiej generalizuje dane,
    tj. daje najmniejszy blad na ciagu walidacyjnym. Wielomian dopasowany jest wg kryterium z regularyzacja. train_err i val_err to
    bledy na sredniokwadratowe na ciagach treningowym i walidacyjnym. regularization_lambda to najlepsza wartosc parametru regularyzacji
    '''
    bestResult = []
    for specificLambda in lambda_values:
        w, train_err = regularized_least_squares(x_train, y_train, M, specificLambda)
        val_err = mean_squared_error(x_val, y_val, w)
        if len(bestResult) < 3 or bestResult[2] > val_err:
            bestResult = (w, train_err, val_err, specificLambda)
    return bestResult
