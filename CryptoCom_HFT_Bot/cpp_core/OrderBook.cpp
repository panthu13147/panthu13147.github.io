#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <string>
#include <sstream>

enum OrderType { BUY, SELL };

class OrderBook {
public:
    std::vector<double> prices;
    void process(double p) {
        prices.push_back(p);
        if (prices.size() > 10) prices.erase(prices.begin());
        
        if (prices.size() == 10) {
            double avg = std::accumulate(prices.begin(), prices.end(), 0.0) / 10;
            double threshold = avg * 0.0001; // 0.01% Filter

            if (p < (avg - threshold)) 
                std::cout << ">>> 🟢 SIGNAL: BUY | Price: " << p << " < Avg: " << avg << std::endl;
            else if (p > (avg + threshold)) 
                std::cout << ">>> 🔴 SIGNAL: SELL | Price: " << p << " > Avg: " << avg << std::endl;
            else 
                std::cout << "Market Stable | BTC: $" << p << std::endl;
        } else {
            std::cout << "Warming up... (" << prices.size() << "/10)" << std::endl;
        }
    }
};

int main() {
    OrderBook book;
    std::string line;
    while (std::getline(std::cin, line)) {
        if (line == "EXIT") break;
        std::stringstream ss(line);
        std::string p_str;
        std::getline(ss, p_str, ','); 
        try { book.process(std::stod(p_str)); } catch (...) {}
    }
    return 0;
}