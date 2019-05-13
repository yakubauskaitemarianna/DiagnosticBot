:- encoding('utf8').

identify(X, UL) :-
    diag(_, X, L_any, L_all, L_without, L_from_to, Nmin, Nmax),
    any(UL, L_any),
    all(UL, L_all),
    without(UL, L_without),
    from_to(UL, L_from_to, Nmin, Nmax),
    !.

member(X, [X|_]).
member(X, [_|T]) :-
    member(X, T).

from_to(_, [0], _, _) :- !.
from_to(_, [], Nmin, Nmax) :-
    Nmin =< 0,
    Nmax >= 0, !.
from_to(UL, [Nsymp|T], Nmin, Nmax) :- write(UL), nl,
    cond(Nsymp, Symp),
    member(Symp, UL),
    N_min = Nmin-1,
    N_max = Nmax-1,
    from_to(UL, T, N_min, N_max),
    !.
from_to(UL, [_|T], Nmin, Nmax) :-
    from_to(UL, T, Nmin, Nmax),
    !.

any(UL, L) :-
    length(L, Nmax),
    from_to(UL, L, 1, Nmax).

all(UL, L) :-
    length(L, N),
    from_to(UL, L, N, N).

without(_, [0]) :- !.
without(UL, L) :-
    not(any(UL, L)).

diag(1, аллергия, [31, 40, 13], [24, 41], [1], [0], 0, 0).
diag(2, аппендицит, [11, 12,  27, 38, 50], [18, 1], [0], [1, 5, 26, 14, 35], 2, 5).
diag(3, диабет, [22, 44, 39], [47, 51, 15], [0], [17, 32, 50, 7, 23], 3, 5).
diag(4, грипп, [11, 27, 50, 17, 14], [18, 13, 4], [0], [21, 32, 30, 17, 41], 0, 0).
diag(5, герпес, [10, 45, 21], [23, 18, 43], [0], [0], 0, 0).
diag(6, вич, [43], [18], [0], [25, 30, 41, 11, 33, 29], 3, 6).
diag(7, волчанка, [25, 37], [18], [0], [4, 32, 30, 17], 2, 4).
diag(8, менопауза, [48, 49, 36], [0], [0], [3, 23, 51], 0, 0).
diag(9, беременность, [17, 20, 21], [2, 17], [0], [5, 9, 19, 28, 32, 50], 3, 6).
diag(10, рак_простаты, [16, 34, 52, 8], [35], [0], [47, 6, 1, 42], 2, 4).


cond(1, abdominal_pain).
cond(2, absent_menstrual_periods).
cond(3, acne).
cond(4, appetite_loss).
cond(5, back_pain).
cond(6, blood_in_urine).
cond(7, blurred_vision).
cond(8, bone_pain).
cond(9, breast_pain).
cond(10, burning).
cond(11, chills).
cond(12, constipation).
cond(13, cough).
cond(14, diarrhea).
cond(15, dry_mouth).
cond(16, erectile_dysfunction).
cond(17, fatigue).
cond(18, fever).
cond(19, food_aversion).
cond(20, frequent_urination).
cond(21, headache).
cond(22, hunger).
cond(23, itch).
cond(24, itchy_eyes).
cond(25, joint_pain).
cond(26, loss_of_appetite).
cond(27, malaise).
cond(28, mood_changes).
cond(29, mouth_ulcers).
cond(30, muscle_pain).
cond(31, nasal_congestion).
cond(32, nausea).
cond(33, night_sweats).
cond(34, painful_ejaculation).
cond(35, pain_urination).
cond(36, painful_sexual_intercourse).
cond(37, rash).
cond(38, rectal_pain).
cond(39, slow_healing_wounds).
cond(40, sneezing).
cond(41, sore_throat).
cond(42, swelling).
cond(43, swollen_lymph_nodes).
cond(44, thirst_changes).
cond(45, tingling).
cond(47, urination_changes).
cond(48, vaginal_dryness).
cond(49, vaginal_irritation).
cond(50, vomiting).
cond(51, weight_changes).
cond(52, weight_loss).
