setreadonly(table, false)
table._remove = function(tbl, key) 
    local Result = {} 
    for Index, Value in tbl do 
        if Index ~= key then 
            table.insert(Result, Value) 
        end 
    end 
    
    tbl = Result
end 

table.removeKey = function(tbl, key) 
    local Result = {} 
    for Index, Value in tbl do 
        if Index ~= key then 
            Result[Index] = Value
        end 
    end 
    
    tbl = Result
end 

table.length = function(tbl) 
    local Count = 0 
    for _ in tbl do 
        Count = Count + 1 
    end 
    
    return Count
end 

table.keys = function(tbl) 
    local Result = {} 
    
    for i in tbl do 
        table.insert(Result, i) 
    end 
    
    return Result
end

table.values = function(tbl)
    local Result = {} 
    
    for _, i in tbl do 
        table.insert(Result, i) 
    end 
    
    return Result
end

table.reverse = function(tbl) 
    local Result = {} 
    
    for u, i in ipairs(tbl) do 
        
        Result[i] = u
        
    end 
    
    return Result
end


table.sum = function(tbl) 
    a = 0 
    for _, v in tbl do
        a = a + v 
    end 
    return a
end 

table.rsort = function(tbl, cb) 
    table.sort(tbl, cb) 
    return tbl 
end 

table.map = function(tbl, cb) 
    local res = {} 
    for i, v in tbl do 
        table.insert(res, cb(i, v)) 
    end 
    
    return res
end 
table.removeValue = function(tbl, key) 
    local Result = {} 
    for Index, Value in tbl do 
        if Value ~= key then 
            Result[Index] = Value
        end 
    end 
    
    tbl = Result
end 

setreadonly(table, true)
