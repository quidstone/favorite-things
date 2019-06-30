from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABdFgE1LIl7kZX2_z1hxNtka3ZbkbP_O9uRx0bKXVUD5MIWeNjvD81qIiLuNxlYE557m3HB-lsAxlNs71kWFoX81ig7OB-UrWRaI5TVbPKaAtik5VCAnVtRwOA9PSz_EIyVI0QPu5lAbpC_VL3_4z07cyqCKefNm4O-YzO7sk3pJ6eCQhY='

def main():
	f = Fernet(key)
	print(f.decrypt(message))

if __name__ == "__main__":
	main()