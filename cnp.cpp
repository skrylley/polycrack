#include <iostream>
#include <cmath>
#include <fstream>
#include <string>
#include <sstream>
using namespace std;

int main()
{
	int c, r, con, cnp;
	int p = 100000000;
	//con = 279146358279;
	unsigned int conV[12] = {2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9};
	unsigned int rezV[12];
	unsigned int cnpV[12];
	cout << "cnp = ";
	cin >> cnp;
	

	for(unsigned int i = 0; i < 9; i++)
	{
		cnpV[i] = cnp / p % 10;
		p = p / 10;
	}
	ostringstream cnp_strBuff;
	cnp_strBuff << cnp;
	//string numeFisier = "cnp_" + cnp_strBuff.str() + "NNNC" + ".csv";
	string numeFisier = cnp_strBuff.str() + ".csv";
	ofstream fout(numeFisier.c_str());

	if (!fout.is_open()) {
        cout << "Eroare la deschiderea fisierului." << endl;
        return 1;
    }
    fout << "CNP;PASS" << endl;



	for(unsigned NNN = 0; NNN <= 999; NNN++)
	{
		c = 0;
		for(unsigned int i = 0; i < 9; i++)
		{
			rezV[i] = cnpV[i] * conV[i];
			c = c + rezV[i];
		}
		
		rezV[ 9] = NNN / 100 % 10 * conV[ 9];
		rezV[10] = NNN / 10 % 10 * conV[10];
		rezV[11] = NNN / 1 % 10 * conV[11];
		
		c = c + rezV[9] + rezV[10] + rezV[11];
		
		r = c % 11;
		c = c / 11;
		
		
		if(r < 10)
			c = r;
			
		if(r == 10)
			c = 1; 
			
		string strBuff;
		ostringstream buffer;
		ostringstream bufferNNN;
		ostringstream bufferC;
		ostringstream buffercnp100;
		
		bufferNNN<<NNN;
		bufferC<<c;
		buffercnp100<<cnp%100;
		

		
		if(NNN < 10)
		{
			//cout<<NNN<<") "<<cnp<<"00"<<NNN<<c<<" | "<<cnp%100<<"00"<<NNN<<c<<"\n";
			strBuff = cnp_strBuff.str() + "00" + bufferNNN.str() + bufferC.str() + ";" + buffercnp100.str() + "00" + bufferNNN.str() + bufferC.str();
			fout << strBuff << endl;
		}
				
		if(NNN >= 10 && NNN < 100)
		{
			//cout<<NNN<<") "<<cnp<<"0"<<NNN<<c<<" | "<<cnp%100<<"0"<<NNN<<c<<"\n";
			strBuff = cnp_strBuff.str() + "0" + bufferNNN.str() + bufferC.str() + ";" + buffercnp100.str() + "0" + bufferNNN.str() + bufferC.str();
			fout << strBuff << endl;
		}
			
		if(NNN >= 100)
		{
			//cout<<NNN<<") "<<cnp<<NNN<<c<<" | "<<cnp%100<<NNN<<c<<"\n";	
			strBuff = cnp_strBuff.str() + bufferNNN.str() + bufferC.str() + ";" + buffercnp100.str() + bufferNNN.str() + bufferC.str();
			fout << strBuff << endl;
		}
	}
   	fout.close();
    cout << "Datele au fost scrise cu succes in fisierul " << numeFisier << "." << endl;
    cin>>c;
    return 0;
}
