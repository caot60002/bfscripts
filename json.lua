local HttpService = game:GetService("HttpService")

local JSON = {}

-- Encoders
local function encodeVector3(v)
	return { __type = "Vector3", x = v.X, y = v.Y, z = v.Z }
end

local function encodeCFrame(cf)
	return { __type = "CFrame", components = { cf:GetComponents() } }
end

-- Decoders
local function decodeVector3(t)
	return Vector3.new(t.x, t.y, t.z)
end

local function decodeCFrame(t)
	return CFrame.new(unpack(t.components))
end

-- Recursive serializer
local function serialize(value)
	local valueType = typeof(value)

	if valueType == "Vector3" then
		return encodeVector3(value)
	elseif valueType == "CFrame" then
		return encodeCFrame(value)
	elseif valueType == "table" then
		local result = {}
		for k, v in pairs(value) do
			result[k] = serialize(v)
		end
		return result
	else
		return value
	end
end

-- Recursive deserializer
local function deserialize(value)
	if typeof(value) == "table" then
		if value.__type == "Vector3" then
			return decodeVector3(value)
		elseif value.__type == "CFrame" then
			return decodeCFrame(value)
		else
			local result = {}
			for k, v in pairs(value) do
				result[k] = deserialize(v)
			end
			return result
		end
	else
		return value
	end
end

-- Public functions
function JSON.stringify(data)
	local serialized = serialize(data)
	return HttpService:JSONEncode(serialized)
end

function JSON.parse(json)
	local decoded = HttpService:JSONDecode(json)
	return deserialize(decoded)
end

return JSON
