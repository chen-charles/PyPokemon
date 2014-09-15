// test.cpp : 

#include "stdafx.h"

int _tmain(int argc, _TCHAR* argv[])
{
	std::cout << "BGRA 2 RGBA (RGBA 2 BGRA) by Charles-Jianye Chen" << std::endl;
	std::wstring uin{};

	if (argc != 2) 
	{
		std::cout << "Input Filename: ";
		std::getline(std::wcin, uin);
		std::cout << std::endl;
	}
	else
	{
		uin = argv[1];
	}

	std::ifstream finx(uin.c_str(), std::ios::binary);
	finx.seekg(0, std::ios::end);      //ÉèÖÃÎÄ¼þÖ¸Õëµ½ÎÄ¼þÁ÷µÄÎ²²¿
	std::streampos ps = finx.tellg();  //¶ÁÈ¡ÎÄ¼þÖ¸ÕëµÄÎ»ÖÃ
	finx.close();

	std::ofstream output(uin.c_str(), std::ios::in | std::ios::out | std::ios::binary);
	std::istream input(output.rdbuf());

	unsigned char r, g, b, a;

	std::cout << "Now Processing ... " << std::endl;
	for (int i = 0; i < ps; i += 4) 
	{
		input.seekg(i);
		r = input.get();
		g = input.get();
		b = input.get();
		a = input.get();

		output.seekp(i);
		output.put(b);
		output.put(g);
		output.put(r);
		output.put(a);
	}
	std::cout << "Done ... " << std::endl;
	input.clear();
	output.close();

	return 0;
}
ÿÿ