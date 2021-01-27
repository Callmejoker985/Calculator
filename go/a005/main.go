package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"net/http"
	"strconv"
	"unicode"
)

var ERROR_EXPRESSION = "1001"
var SUCCESS = "2000"
var msgCodeTable = map[string]string {
	ERROR_EXPRESSION: "表达式错误",
	SUCCESS: "计算成功",
}

func main(){
	registRouter()                                  // 注册路由
	error := http.ListenAndServe(":8080", nil)  // 启动服务器，监听端口
	fmt.Println()
	handleError(error)
}

func registRouter(){
	http.HandleFunc("/index", HandleIndex)
	http.Handle("/js/", http.StripPrefix("/js/", http.FileServer(http.Dir("./js"))))
	http.HandleFunc("/result", HandleGetValue)
}

func HandleGetValue(w http.ResponseWriter, r *http.Request){
	log.Println("【请求】/result，【method】" + r.Method)
	if r.Method == "GET" {
		if err:=r.ParseForm(); err!=nil {
			log.Println("【error】参数解析失败！")
			return
		}
		expression := r.Form["expression"][0]        // 获取前端数据
		log.Println("【expression】" + expression)
		msgCode, value := GetValueByExpression(expression)
		resultMap := map[string]string{
			"MsgCode": msgCode,
			"result": strconv.FormatFloat(value, 'f', 2, 32),
		}
		resultJson, _ := json.Marshal(resultMap)
		fmt.Fprintf(w, string(resultJson))
	}
}

func GetValueByExpression(expression string) (string, float64){
	if len(expression)>1 && expression[0] == '-'{
		expression = "0" + expression
	}
	resultStack := make([]string, 0)
	operateStack, top := make([]string, len(expression)), -1
	lastIndex := len(expression)
	// 中缀转后缀
	for i:=0; i<lastIndex;  i++{
		switch {
		case unicode.IsDigit(rune(expression[i])):   // 如果是数字，直接输出到结果字符串中
			beginIndex := i
			for i<lastIndex && isNumber(expression[i]){
				i++
			}
			if i<lastIndex && expression[i] == '.' {    // 是浮点数
				i++ // 跳过'.'
				for i<lastIndex && isNumber(expression[i]){
					i++
				}
			}
			numStr := expression[beginIndex: i]
			resultStack = append(resultStack, numStr)
			i-- // 回退
		case expression[i] == '(':     // 遇到左括号直接入栈
			top++
			operateStack[top] = string(expression[i])
		case expression[i] == ')':     // 遇到右括号将操作栈中，第一个左括号之前的符号输出
			for operateStack[top] != "("  {
				resultStack = append(resultStack, operateStack[top])
				top--
			}
			top-- // 将左括号出栈
		case expression[i]=='+' || expression[i]=='-': // +、-是低优先级的操作符，因此要将栈中的高优先级操作符先出栈
			for top > -1 && operateStack[top]!=string(expression[i]) && operateStack[top]!="(" {
				resultStack = append(resultStack, operateStack[top])
				top--
			}
			top++
			operateStack[top] = string(expression[i])    // 将+、-操作符入栈
		case expression[i]=='*' || expression[i]=='/':// 遇到乘除、函数都直接入栈
			top++
			operateStack[top] = string(expression[i])
		default:   // 遇到函数的情况。如上所述，直接入栈。
			beginIndex := i
			for unicode.IsLetter(rune(expression[i])) {
				i++
			}
			top++
			operateStack[top] = expression[beginIndex: i]
			i-- // 回退
		}
	}

	for top >= 0 {  // 将剩余的符号输出到结果字符串中
		resultStack = append(resultStack, operateStack[top])
		top--
	}

	// 计算后缀表达式的值
	valueStack := make([]float64, len(expression))
	top = -1
	for i:=0; i<len(resultStack); i++ {
		curStr := resultStack[i]
		if unicode.IsDigit(rune(curStr[0])) { // 当前元素是否为数值，直接入栈
			value, _ := strconv.ParseFloat(curStr, 32)
			top++
			valueStack[top] = float64(value)
		} else if curStr == "+" || curStr=="-" || curStr== "*" || curStr == "/"{ // 如果是双元操作符，将valueStack顶部两个栈出栈
			if top == 0 {
				return "1000", 0  // 需要两个数进行操作，却只有一个数，则表达式错误
			}
			secondValue := valueStack[top]
			top--
			topValue := valueStack[top]
			var newValue float64 = 0.0
			switch curStr {
			case "+": newValue = topValue + secondValue
			case "-": newValue = topValue - secondValue
			case "*": newValue = topValue * secondValue
			case "/": newValue = topValue / secondValue
			}
			valueStack[top] = newValue
		} else {  // 当前操作符为函数
			topValue := valueStack[top]
			var newValue float64 = 0.0
			switch curStr {
			case "sin": newValue = math.Sin(topValue)
			case "cos": newValue = math.Cos(topValue)
			case "sqrt": newValue = math.Sqrt(topValue)
			}
			valueStack[top] = newValue
		}
	}
	return "2000", valueStack[0]
}

func isOperateChar(u uint8) bool {
	if u == '+' || u == '-' || u == '*' || u == '/' {
		return true
	}
	return false
}


func isNumber(targetChar uint8) bool {
	if value:=targetChar-'0'; value<=9 {
		return true
	}
	return false
}


func handleError(err error){
	if err != nil {
		log.Fatalln(err)
	}
}


func HandleIndex(w http.ResponseWriter, r *http.Request){
	log.Println("【页面】index")
	index_byte, err := ioutil.ReadFile("index.html")
	if err != nil {
		_, _ = fmt.Fprintf(w, "服务器读取文件异常")
	} else {
		index_page := string(index_byte)
		_, _ = fmt.Fprintf(w, index_page)
	}
}




