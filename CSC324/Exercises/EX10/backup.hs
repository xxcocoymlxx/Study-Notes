--case of only one parameter
cpsEval env (App proc [arg]) k = cpsEval env proc (\res -> case res of
    Procedure (Proc f) -> (cpsEval env arg (\first_arg -> (f [first_arg] k)))
    _                  -> Error "app")

--case of exactly two parameters
cpsEval env (App proc [param1,param2]) k = cpsEval env proc (\res -> case res of
    Procedure (Proc f) -> (cpsEval env param1 (\arg1 -> 
                                                   cpsEval env param2
                                                   (\arg2 -> (f [arg1,arg2] k))))
    _                  -> Error "app")

--case of exactly 3 parameters
cpsEval env (App proc [param1,param2, param3]) k = cpsEval env proc (\res -> case res of
    Procedure (Proc f) -> (cpsEval env param1 (\arg1 -> 
                                                   cpsEval env param2
                                                   (\arg2 -> 
                                                   cpsEval env param3
                                                   (\arg3 -> (f [arg1,arg2,arg3] k)))))
    _                  -> Error "app")