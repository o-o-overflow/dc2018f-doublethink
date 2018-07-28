int main()
{
	int(*open)(int,int) = 0x9860;
	int(*read)(int,int,int) = 0x7980;
	int(*write)(int,int,int) = 0x7a20;
	int f = open(0x10200, 0);
	write(0, 0x10200, read(f, 0x10200, 1024));
}
