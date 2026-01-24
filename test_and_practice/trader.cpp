#include<iostream>
#include<cstdlib>
#include<ctime>
#include<unistd.h>
using namespace std;
int main (){
    srand(time(0));
    double balance = 10000;
    cout<<"-----HFT bot starting-----"<<endl;
    cout<<"target: buy ETH if the price is below $2000"<<endl;
    cout << "Starting Balance: $" << balance << endl;
    cout << "------------------------" << endl;
    while(balance>500)
    {int current_price = (rand()%2000)+1000; // Simulate ETH price between $1000 and $2999
        cout << "Market Price: $" << current_price << " ... ";
        if (current_price < 2000)
        {
            cout << "Buying ETH!" << endl;
            balance =balance - current_price ; // Buy 0.1 ETH
            cout << "--> Remaining Balance: $" << balance << endl;
        } else {
            cout<<"too expensive, waiting."<<endl;

        }
        sleep(1);

    }
    cout << "------------------------" << endl;
    cout << "Wallet Drained. Bot Stopping." << endl;

       
    return 0;
}