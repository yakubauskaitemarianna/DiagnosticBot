domains
	user_list = symbol*
	symp_list = integer*
	
predicates
	identify(symbol, user_list)
	member(symbol, user_list)
	length(integer, symp_list)
	from_to(user_list, symp_list, integer, integer)
	any(user_list, symp_list)
	all(user_list, symp_list)
	without(user_list, symp_list)
	diag(integer, symbol, symp_list, symp_list, symp_list, symp_list, integer, integer)
	cond(integer, symbol)

clauses
	identify(X, UL) :- diag(_, X, L_any, L_all, L_without, L_from_to, Nmin, Nmax), 
				any(UL, L_any),
				all(UL, L_all),
				without(UL, L_without),
				from_to(UL, L_from_to, Nmin, Nmax), !.
	
	member(X, [X|_]).
	member(X, [_|T]) :- member(X, T).
	
	length(0, []).
	length(N, [_|T]) :- length(N1, T), N = N1+1.
	
	%from_to(Nmin, _, [], _) :- Nmin > 0, fail.
	%from_to(_, Nmax, [], _) :- Nmax < 0, fail.
	from_to(_, [0], _, _) :- !.
	from_to(_, [], Nmin, Nmax) :- Nmin <= 0, Nmax >= 0, !.
	from_to(UL, [Nsymp|T], Nmin, Nmax) :- cond(Nsymp, Symp), member(Symp, UL), N_min = Nmin-1, N_max = Nmax-1, from_to(UL, T, N_min, N_max), !.
	from_to(UL, [_|T], Nmin, Nmax) :- from_to(UL, T, Nmin, Nmax), !.
	
	any(UL, L) :- length(Nmax, L), from_to(UL, L, 1, Nmax).
	
	all(UL, L) :- length(N, L), from_to(UL, L, N, N).
	
	without(_, [0]) :- !.
	without(UL, L) :- not(any(UL, L)).
	
        diag(8, allergy, [31, 42, 13], [24, 41], [1], [0], 0, 0).
	diag(1, herpes, [0], [0], [0], [0], 0, 0).
        diag(2, pregnancy, [0], [0], [0], [0], 0, 0).
        diag(3, menopause, [0], [0], [0], [0], 0, 0).
        diag(4, deabetes, [0], [0], [0], [0], 0, 0).
        diag(5, lupus, [0], [0], [0], [0], 0, 0).
        diag(6, hIV, [0], [0], [0], [0], 0, 0).
        diag(7, proctate_cancer, [0], [0], [0], [0], 0, 0).
        diag(9, flu, [0], [0], [0], [0], 0, 0).
        diag(10, appendicitis, [0], [0], [0], [0], 0, 0).
        
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
        cond(34, pain_urination).
        cond(35, painful_ejaculation).
        cond(36, painful_rination).
        cond(37, painful_sexual_intercourse).
        cond(38, rash).
        cond(39, rectal_pain).
        cond(40, slow_healing_wounds).
        cond(41, sneezing).
        cond(42, sore_throat).
        cond(43, swelling).
        cond(44, swollen_lymph_nodes).
        cond(45, thirst_changes).
        cond(46, tingling).
        cond(47, tiredness).
        cond(48, urination_changes).
        cond(49, vaginal_dryness).
        cond(50, vaginal_irritation).
        cond(51, vomiting).
        cond(52, weight_changes).
        cond(53, weight_loss).
	

goal
	identify(X, [itchy_eyes, sneezing, cough]).