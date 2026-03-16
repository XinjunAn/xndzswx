void Widget::on_btn_check_algebra_clicked()
{
    QStringList rawElements = ui->lineEdit_elements->text().split(QRegularExpression("[,，]"), Qt::SkipEmptyParts);
    QStringList elements;
    std::map<QString, int> elementMap;

    for (const QString& s : rawElements) {
        QString clean = s.trimmed();
        if (!clean.isEmpty() && !elementMap.count(clean)) {
            elementMap[clean] = elements.size();
            elements << clean;
        }
    }

    int n = elements.size();
    if (n == 0) { QMessageBox::warning(this, "提示", "请先输入集合元素。"); return; }

    std::vector<std::vector<int>> table(n, std::vector<int>(n, -1));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            QTableWidgetItem *item = ui->tableWidget_algebra->item(i, j);
            QString cellValue = (item) ? item->text().trimmed() : "";

            if (cellValue.isEmpty() || !elementMap.count(cellValue)) {
                QMessageBox::critical(this, "数据校验失败",
                                      QString("坐标 (%1, %2) 输入无效。\n内容: '%3'\n有效集合: {%4}")
                                          .arg(i+1).arg(j+1).arg(cellValue).arg(elements.join(",")));
                return;
            }
            table[i][j] = elementMap[cellValue];
        }
    }

    bool isCommutative = true;
    bool isAssociative = true;

    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if (table[i][j] != table[j][i]) { isCommutative = false; break; }

    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            for (int k = 0; k < n; ++k)
                if (table[table[i][j]][k] != table[i][table[j][k]]) { isAssociative = false; goto end_loop; }
end_loop:;

    int identity = -1;
    for (int e = 0; e < n; ++e) {
        bool ok = true;
        for (int a = 0; a < n; ++a) if (table[e][a] != a || table[a][e] != a) { ok = false; break; }
        if (ok) { identity = e; break; }
    }

    int zero = -1;
    for (int z = 0; z < n; ++z) {
        bool ok = true;
        for (int a = 0; a < n; ++a) if (table[z][a] != z || table[a][z] != z) { ok = false; break; }
        if (ok) { zero = z; break; }
    }

    QString invSummary = "无";
    if (identity != -1) {
        QStringList invs;
        for (int i = 0; i < n; ++i) {
            int invIdx = -1;
            for (int j = 0; j < n; ++j)
                if (table[i][j] == identity && table[j][i] == identity) { invIdx = j; break; }
            invs << QString("%1?1=%2").arg(elements[i]).arg(invIdx == -1 ? "无" : elements[invIdx]);
        }
        invSummary = invs.join(", ");
    } else {
        invSummary = "（无幺元，不讨论逆元）";
    }

    QString html = QString(R"(
        <div style="font-family: 'Microsoft YaHei'; text-align: center; padding: 15px;">
            <div style="font-size: 20px; color: #2c3e50; line-height: 1.5;">
                <div style="margin: 8px 0;"><b>交换律：</b> <span style="color: %1;">%2</span></div>
                <div style="margin: 8px 0;"><b>结合律：</b> <span style="color: %3;">%4</span></div>
                <div style="margin: 8px 0;"><b>幺元 (e)：</b> <span style="color: #2980b9;">%5</span></div>
                <div style="margin: 8px 0;"><b>零元 (θ)：</b> <span style="color: #2980b9;">%6</span></div>

                <div style="margin-top: 25px; padding: 15px; background-color: #f9f9f9; border-radius: 8px; border: 1px solid #eee;">
                    <b style="font-size: 20px;">逆元分析：</b><br>
                    <div style="color: #2980b9; font-size: 18px; margin-top: 10px;">%7</div>
                </div>
            </div>
        </div>
    )").arg(isCommutative ? "#27ae60" : "#c0392b").arg(isCommutative ? "满足" : "不满足")
                       .arg(isAssociative ? "#27ae60" : "#c0392b").arg(isAssociative ? "满足" : "不满足")
                       .arg(identity == -1 ? "无" : elements[identity])
                       .arg(zero == -1 ? "无" : elements[zero])
                       .arg(invSummary);

    ui->textBrowser_algebra->setHtml(html);
}
