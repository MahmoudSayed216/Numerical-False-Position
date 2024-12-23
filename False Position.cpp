#include<iostream>
#include<iomanip>
#include<cmath>
#include<limits>
#include"./muparser/include/muParser.h"

#define EPSILON 0.1
#define ALPHA 0.01
#define PRECISION 10
#define STEP_SIZE 0.001

std::string expression;
mu::Parser parser;
double var;


// im going to use double instead of float accross the file to improve the accuracy of the calculations


void log_with_high_precision(std::string txt, double val){
    std::cout << txt << std::fixed <<std::setprecision(PRECISION) << val << '\n';
}


double f(double x){
    var = x;
    return parser.Eval();
}


bool approximately_equal_to_zero(double val){
    log_with_high_precision("val: ", val);
    return std::fabs(val) <= EPSILON  ;
}


void log_iteration_info(double a, double b, double c){
    log_with_high_precision("f(a) = ", f(a));    
    log_with_high_precision("f(b) = ", f(b));  
    std::cout << "\n";

    double delta_y = f(b) - f(a);
    double delta_x = b - a;
    double slope = delta_y/delta_x;
    
    log_with_high_precision("a = ", a);
    log_with_high_precision("b = ", b);
    log_with_high_precision("c = ", c);
    std::cout << "\n";
    log_with_high_precision("delta y: ",delta_y);
    log_with_high_precision("delta x: ",delta_x);
    log_with_high_precision("slope: ", slope);
    std::cout << "\n";
    


    if(f(a) * f(c) < 0) // a and c have opposite signs, hence c replaces b
    { 
        std::cout << "f(b) and f(c) have the same sign, so c replaces b\n";
    }
    else // the opposite, hence c replaces a
    {
        std::cout << "f(a) and f(c) have the same sign, so c replaces a\n";
    }

}


void begin_false_position(double a, double b, bool log_info_flag){

    double c;
    unsigned int n_iters = 0;
    
    while(1){
        n_iters++;
        //the iterative formula
        c = b - f(b)*(b-a) / (f(b)-f(a));

        log_with_high_precision("c = ", c);
        log_with_high_precision("f(c) = ", f(c));

        if(std::fabs(f(c)) <= ALPHA)
            break;

        if(log_info_flag) log_iteration_info(a, b, c);

        if(f(a) * f(c) < 0){
            a = c;
        }
        else{
            b = c;
        }
        std::cout << "________________________\n";

    }

    std::cout << "\n\n";
    std::cout << "************************************\n";
    std::cout << "***                              ***\n";
    std::cout << "***    root    = "  << c << "    ***\n";
    std::cout << "***    f(root) = " << f(c) << "   ***\n"; 
    std::cout << "*** ____________________________ ***\n";
    std::cout << "***                              ***\n";
    std::cout << "***    Number of iterations: " << n_iters << "  ***\n";
    std::cout << "***                              ***\n";
    std::cout << "************************************\n";

}



bool is_continuous(double a, double  b){
    for(double p = a; p <= b; p+=STEP_SIZE){
        double left_limit = f(p - ALPHA);
        double right_limit = f(p + ALPHA);
        double actual = f(p);

        if(std::isnan(left_limit) or std::isnan(right_limit) or std::isnan(actual)  or  std::isinf(left_limit) or std::isinf(right_limit) or std::isinf(actual))
            return false;

        //check if any of the values is equal to -nan or inf
        log_with_high_precision("x: ", p);
        log_with_high_precision("left: ", left_limit);
        log_with_high_precision("right: ", right_limit);
        log_with_high_precision("actual: ", actual);



        if(!approximately_equal_to_zero(actual - left_limit))
            return false;
        if(!approximately_equal_to_zero(actual - right_limit))
            return false;

    }
    std::cout << "is cts\n";
    
    return true;
}


bool unequal_signs(double a, double  b){
    return f(a)*f(b) < 0;
}

bool sign(double v){
    return v < 0;
}


int number_of_roots(double a, double  b){
    int roots = 0;
    bool is_neg = sign(f(a));
    std::cout << "initial sign: " << is_neg << '\n';
    
    for(double i = a; i <= b; i+=STEP_SIZE){
        std::cout << "V: " << f(i) << '\n';
        std::cout << "sign: " << sign(f(i)) << '\n';
        std::cout << "is negative: " << is_neg << '\n';
        std::cout << "roots: " << roots << '\n';
        if(sign(f(i)) != is_neg){
            roots+=1;
            is_neg = !is_neg;
        }
    }
    // roots += (f(a) == 0 || f(b) == 0);
    return roots;
}


bool is_workable(double a, double  b){
    bool _cts = is_continuous(a, b);
    bool _unequal_signs = unequal_signs(a, b); 
    int _n_roots = number_of_roots(a, b);
    std::cout << "cts: " << _cts << '\n';
    std::cout << "unequal signs: " << _unequal_signs<<'\n';
    std::cout << "one root: " << _n_roots << '\n';

    if(!_cts)
        std::cout << "f(x)  = " << expression << " is not workable due to a discontinuity at {placeholder}\n";
    if(!_unequal_signs) // if signs are equal
        std::cout << "f(x)  = " << expression << " is not workable because the signs of f(" << a << ") and f(" << b << ") are equal\n";
    if(_n_roots > 1)
        std::cout << "f(x)  = " << expression << " is not workable because it has more than one root on the given interval\n";


    return _cts and _unequal_signs and _n_roots ==1;
}


void cap_x(std::string &expr){
    for(char &c: expr){
        if(toupper(c) == 'X')
            c = toupper(c);
    }
}


int main(){
    std::cout << "Enter and expression (The variable should be X): ";
    std::cin >> expression;
    cap_x(expression);

    parser.SetExpr(expression);
    
    parser.DefineVar("X", &var);

    std::cout << "Enter the interval, lower limit then upper limit\n";
    double a, b;// a-> lower limit, b-> upper limit
    std::cin >> a >> b;
    std::cout << "\n\n";

    // std::string  func = "x*sin(x) - 1";
    log_with_high_precision("STEP_SIZE: ", STEP_SIZE);
    if(is_workable(a, b)){
        std::cout << "False Position is workable.\n";
        std::cout << "f(x) =  " << expression << '\n';
        std::cout << "Interval: " << "[ " << a << ", " << b << "]\n\n";  
        std::cout << "Logging precision: " << PRECISION << '\n';
        std::cout << "Starting False Position\n";
        std::cout << "********************\n"; 
        begin_false_position(a, b, true);
    }
    else{
        std::cout << "False Position is NOT workable\n";
    }

    return 0;
}