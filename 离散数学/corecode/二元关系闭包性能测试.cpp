void Widget::on_btn_calc_relation_clicked()
{
    bool okN, okM;
    int n = ui->lineEdit_N->text().toInt(&okN);
    int m = ui->lineEdit_M->text().toInt(&okM);

    if (!okN || !okM || n <= 0 || m < 0) {
        QMessageBox::warning(this, "参数错误", "请输入有效的正整数 N 和非负整数 M。");
        return;
    }

    ui->textBrowser_relation->setText("正在执行性能测试，请稍候...");
    QCoreApplication::processEvents();

    mat a(n, std::vector<char>(n, 0));
    std::chrono::high_resolution_clock::time_point start_all = std::chrono::high_resolution_clock::now();
    std::mt19937_64 rng(start_all.time_since_epoch().count());
    std::uniform_int_distribution<int> dist(0, n - 1);
    for(int i = 0; i < m; ++i) {
        a[dist(rng)][dist(rng)] = 1;
    }

    using clk = std::chrono::high_resolution_clock;
    const int iterations = 1000;
    double t_reflexive = 0, t_symmetric = 0;

    for(int i = 0; i < iterations; ++i) {
        mat r_mat = a;
        auto s = clk::now();
        for(int j = 0; j < n; ++j) r_mat[j][j] = 1;
        auto e = clk::now();
        t_reflexive += std::chrono::duration<double>(e - s).count();

        mat s_mat(n, std::vector<char>(n, 0));
        auto s2 = clk::now();
        for(int r = 0; r < n; ++r) {
            for(int c = 0; c < n; ++c) {
                if(a[r][c]) s_mat[r][c] = s_mat[c][r] = 1;
            }
        }
        auto e2 = clk::now();
        t_symmetric += std::chrono::duration<double>(e2 - s2).count();
    }
    auto s_iter = clk::now();
    mat tc_iter = a;
    mat pA = a;
    for(int i = 1; i < n; ++i) {
        pA = mat_multiply(pA, a, n);
        for(int r = 0; r < n; ++r)
            for(int c = 0; c < n; ++c)
                tc_iter[r][c] = tc_iter[r][c] || pA[r][c];
    }
    auto e_iter = clk::now();
    double dur_iter = std::chrono::duration<double>(e_iter - s_iter).count();

    auto s_warshall = clk::now();
    mat tc_warshall = a;
    for(int k = 0; k < n; ++k) {
        for(int i = 0; i < n; ++i) {
            for(int j = 0; j < n; ++j) {
                tc_warshall[i][j] = tc_warshall[i][j] || (tc_warshall[i][k] && tc_warshall[k][j]);
            }
        }
    }
    auto e_warshall = clk::now();
    double dur_warshall = std::chrono::duration<double>(e_warshall - s_warshall).count();

    QString report = QString(R"(
        <div style="font-family: 'Segoe UI', sans-serif; line-height: 1.6;">
            <div style="border-bottom: 2px solid #2c3e50; padding-bottom: 5px; margin-bottom: 15px;">
                <span style="font-size: 12px; color: #7f8c8d; float: right;">%1</span>
            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                <tr style="background-color: #f8f9fa;">
                    <td style="padding: 8px; border: 1px solid #dee2e6;"><b>集合规模 (N)</b></td>
                    <td style="padding: 8px; border: 1px solid #dee2e6;">%2 阶方阵</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6;"><b>关系总数 (M)</b></td>
                    <td style="padding: 8px; border: 1px solid #dee2e6;">%3 条边</td>
                </tr>
            </table>

            <br>
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
                <tr style="background-color: #34495e; color: white;">
                    <th style="padding: 10px; border: 1px solid #2c3e50;">闭包类型 (Closure)</th>
                    <th style="padding: 10px; border: 1px solid #2c3e50;">算法复杂度</th>
                    <th style="padding: 10px; border: 1px solid #2c3e50;">平均单次耗时 (sec)</th>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #dee2e6;">自反闭包 (Reflexive)</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6;">O(N)</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6; color: #2980b9;">%4</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #dee2e6;">对称闭包 (Symmetric)</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6;">O(N2)</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6; color: #2980b9;">%5</td>
                </tr>
                <tr style="background-color: #fff9f9;">
                    <td style="padding: 8px; border: 1px solid #dee2e6;">传递闭包 (Iteration)</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6;">O(N?)</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6; color: #c0392b; font-weight: bold;">%6</td>
                </tr>
                <tr style="background-color: #f4fbf4;">
                    <td style="padding: 8px; border: 1px solid #dee2e6;">传递闭包 (Warshall)</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6;">O(N3)</td>
                    <td style="padding: 8px; border: 1px solid #dee2e6; color: #27ae60; font-weight: bold;">%7</td>
                </tr>
            </table>

            <div style="margin-top: 15px; padding: 10px; background-color: #f1f2f6; border: 1px solid #dcdde1; font-size: 12px;">
                <b>实验结论：</b> 在当前规模下，Warshall 算法的执行效率约为矩阵幂迭代法的 <b>%8</b> 倍。
                该结果验证了理论时间复杂度的显著差异。
            </div>
        </div>
    )")
                         .arg(QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss"))
                         .arg(n).arg(m)
                         .arg(t_reflexive / iterations, 0, 'f', 8)
                         .arg(t_symmetric / iterations, 0, 'f', 8)
                         .arg(dur_iter, 0, 'f', 6)
                         .arg(dur_warshall, 0, 'f', 6)
                         .arg(dur_iter / (dur_warshall + 1e-9), 0, 'f', 2);

    ui->textBrowser_relation->setHtml(report);
}
