void Widget::on_btn_calc_inference_clicked()
{

    QString qsP = ui->lineEdit_premises->text().replace(" ", "").replace("，", ",");
    QString qsC = ui->lineEdit_conclusion->text().replace(" ", "");

    if(qsP.isEmpty() || qsC.isEmpty()) {
        QMessageBox::warning(this, "输入为空", "前提集合与结论均不能为空。");
        return;
    }

    for(int i = 0; i < qsP.length() - 1; ++i) {
        if(qsP[i].isLetter() && qsP[i] == qsP[i+1]) {
            QMessageBox::critical(this, "语法错误", QString("前提中检测到连续重复变元 '%1%1'，请检查输入是否正确。").arg(qsP[i]));
            return;
        }
    }
    for(int i = 0; i < qsC.length() - 1; ++i) {
        if(qsC[i].isLetter() && qsC[i] == qsC[i+1]) {
            QMessageBox::critical(this, "语法错误", QString("结论中检测到连续重复变元 '%1%1'，请检查输入。").arg(qsC[i]));
            return;
        }
    }
    QRegularExpression regex("^[A-Za-z!\\+\\*\\>~,\\(\\)]+$");
    if(!regex.match(qsP).hasMatch() || !regex.match(qsC).hasMatch()) {
        QMessageBox::critical(this, "非法字符",
                              "检测到不支持的字符！\n\n可用符号：\n1. 命题变元：A-Z 或 a-z\n2. 逻辑运算符：! + * > ~\n3. 辅助符号：( ) 和英文逗号");
        return;
    }

    QString premises = qsP;
    QString combinedPremises = "(" + premises.replace(",", ")*(") + ")";
    QString fullFormula = "(" + combinedPremises + ")>(" + qsC + ")";

    std::string s = fullFormula.toStdString();
    std::vector<char> postFix;
    std::vector<char> opStack;
    std::set<char> vars;

    for(char i : s) {
        if(isalpha(i) && i != 'T' && i != 'F') {
            postFix.push_back(i);
            vars.insert(i);
        }
        else if(i == '(') opStack.push_back(i);
        else if(QString("!+*>~").contains(i)) {
            while(!opStack.empty() && logic_val(opStack.back()) >= logic_val(i)) {
                postFix.push_back(opStack.back());
                opStack.pop_back();
            }
            opStack.push_back(i);
        }
        else if(i == ')') {
            while(!opStack.empty() && opStack.back() != '(') {
                postFix.push_back(opStack.back());
                opStack.pop_back();
            }
            if(!opStack.empty()) opStack.pop_back();
        }
    }
    while(!opStack.empty()) { postFix.push_back(opStack.back()); opStack.pop_back(); }

    if(vars.empty()) {
        QMessageBox::warning(this, "解析失败", "公式中未检测到有效命题变元。");
        return;
    }

    if(vars.size() > 10) {
        QMessageBox::warning(this, "变元过多",
                             QString("检测到 %1 个不同变元。为防止计算卡死，请将变元总数限制在 10 个以内。").arg(vars.size()));
        return;
    }

    std::vector<char> orderList(vars.begin(), vars.end());
    std::map<char, int> vMap;
    for(int i = 0; i < (int)orderList.size(); ++i) vMap[orderList[i]] = i;

    int n = orderList.size();
    bool isValid = true;
    for(int i = 0; i < (1 << n); ++i) {
        std::vector<int> currentAy(n);
        for(int j = 0; j < n; ++j) currentAy[j] = (i >> (n - 1 - j)) & 1;

        std::vector<int> resStack;
        for(char c : postFix) {
            if(isalpha(c)) resStack.push_back(currentAy[vMap[c]]);
            else if(c == '!') {
                if(resStack.empty()) return;
                int x = resStack.back(); resStack.pop_back();
                resStack.push_back(!x);
            }
            else {
                if(resStack.size() < 2) continue;
                int y = resStack.back(); resStack.pop_back();
                int x = resStack.back(); resStack.pop_back();
                if(c == '*') resStack.push_back(x && y);
                else if(c == '+') resStack.push_back(x || y);
                else if(c == '>') resStack.push_back(!x || y);
                else if(c == '~') resStack.push_back(x == y);
            }
        }
        if(!resStack.empty() && resStack.back() == 0) { isValid = false; break; }
    }

    QString varListStr;
    for(char c : orderList) varListStr += QString(c) + " ";

    QString resultStatus = isValid ?
                               "<b style='color: #27ae60;'>✔️ 推理有效 (Valid)</b>" :
                               "<b style='color: #c0392b;'>❌ 推理无效 (Invalid)</b>";

    ui->textBrowser_inference->setHtml(QString(R"(
        <div style="font-family: 'Microsoft YaHei'; text-align: center; padding: 15px;">
            <p style="font-size: 14px; color: #7f8c8d;">识别到的命题变元: <span style="color: #2c3e50;">%1</span></p>
            <p style="font-size: 16px; color: #7f8c8d; margin-top: 10px;">转化后逻辑公式</p>
            <code style="font-size: 18px; color: #2980b9; background: #f4f7f9; padding: 5px 12px; border: 1px dotted #abc;">%2</code>
            <div style="margin: 25px 0;"><p style="font-size: 16px; color: #7f8c8d;">判定结论</p><div style="font-size: 26px;">%3</div></div>
        </div>
    )").arg(varListStr).arg(fullFormula).arg(resultStatus));
}