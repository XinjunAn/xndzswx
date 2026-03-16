void Widget::on_btn_calc_set_clicked()
{
    a1.clear(); b1.clear(); cu.clear(); ci.clear(); cx.clear();

    QString qStrA = ui->lineEdit_A->text().trimmed();
    QString qStrB = ui->lineEdit_B->text().trimmed();
    if(qStrA.isEmpty() || qStrB.isEmpty()) {
        QMessageBox::warning(this, "输入为空", "集合 A 和集合 B 不能为空！\n请输入英文字母元素。");
        return;
    }
    auto checkInput = [](const QString& str) -> QString {
        bool lastWasLetter = false;
        for (QChar c : str) {
            ushort u = c.unicode();
            bool isEng = (u >= 'a' && u <= 'z') || (u >= 'A' && u <= 'Z');
            bool isChinese = (u >= 0x4E00 && u <= 0x9FA5);
            bool isSep = c.isSpace() || c == ',' || c == ';' || QString("，；").contains(c);

            if (isEng) {
                if (lastWasLetter) {
                    return "元素之间必须用分隔符（如空格、逗号或中文）隔开！\n错误示例：连续输入了两个字母。";
                }
                lastWasLetter = true;
            }
            else if (isChinese || isSep) {
                lastWasLetter = false;
            }
            else {
                return QString("检测到非法字符：'%1'\n请勿输入数字或不支持的特殊符号！").arg(c);
            }
        }
        return "";
    };

    QString errorA = checkInput(qStrA);
    if (!errorA.isEmpty()) {
        QMessageBox::critical(this, "集合 A 格式错误", errorA);
        return;
    }

    QString errorB = checkInput(qStrB);
    if (!errorB.isEmpty()) {
        QMessageBox::critical(this, "集合 B 格式错误", errorB);
        return;
    }
    a = qStrA.toStdString();
    b = qStrB.toStdString();

    int la=a.size(), lb=b.size();
    for(int i=0; i<la; i++) {
        if((a[i]>='a'&&a[i]<='z')||(a[i]>='A'&&a[i]<='Z'))
            a1.insert(a[i]);
    }
    for(int i=0; i<lb; i++) {
        if((b[i]>='a'&&b[i]<='z')||(b[i]>='A'&&b[i]<='Z'))
            b1.insert(b[i]);
    }
    if(a1.empty() || b1.empty()) {
        QMessageBox::critical(this, "格式错误", "未检测到有效的英文字母集合元素！");
        return;
    }

    union1();
    intersection();
    vector<char> cd = difference();
    cx = xor1();

    QString outStr = "";

    outStr += "A*B={";
    for(size_t i=0; i<ci.size(); i++) {
        outStr += ci[i];
        if(i != ci.size()-1) outStr += ",";
    }
    outStr += "}\n";

    outStr += "A+B={";
    bool first = true;
    for (char x : cu) {
        if (!first) outStr += ",";
        outStr += x;
        first = false;
    }
    outStr += "}\n";

    outStr += "A-B={";
    for(size_t i=0; i<cd.size(); i++) {
        outStr += cd[i];
        if(i != cd.size()-1) outStr += ",";
    }
    outStr += "}\n";

    outStr += "A~B={";
    for(size_t i=0; i<cx.size(); i++) {
        outStr += cx[i];
        if(i != cx.size()-1) outStr += ",";
    }
    outStr += "}";
    ui->textBrowser_out->setText(outStr);
}
