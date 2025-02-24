#include <thread>
#include <mutex>
#include <iostream>
#include <condition_variable>

void print_numbers(int number) {
    std::cout << number << std::endl;
}

int MAX_NUMBER = 50;
std::mutex print_mutex;
bool print_odd_flag = true;
std::condition_variable cv;

void print_action(bool print_odd) {
    for (int i = print_odd ? 1 : 2; i <= MAX_NUMBER; i+=2) {
        std::unique_lock<std::mutex> lock(print_mutex);
        cv.wait(lock, [print_odd](){return print_odd_flag == print_odd;});
        print_numbers(i);
        print_odd_flag = ! print_odd;
        cv.notify_one();
    }
}

void print_odd() {
    print_action(true);
}

void print_even() {
    print_action(false);
}

int main() {
    std::thread print_odd_thread(print_odd);
    std::thread print_even_thread(print_even);
    print_odd_thread.join();
    print_even_thread.join();
    return 0;
}