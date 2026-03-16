#include <QTableWidget>
#include <QTableWidgetItem>
#include <QHeaderView>

vector<char> a_logic;
vector<char> order;
map<char, int> mirror;
string s_logic;
vector<char> b_logic;
int n_logic = 0;
vector<int> ay;
vector<int> calc;
int x, y;
set<char> unique_vars;

vector<vector<int>> table_data;
QString error_msg = "";

int no(int v) { return !v; }
int hequ(int v,int w) { return v&&w; }
int xiqu(int v,int w) { return v||w; }
int yunhan(int v,int w) { return (!v)||w; }
int dengjia(int v,int w) { return v==w; }

int value(char c) {
    if(c=='!') return 4;
    else if(c=='*') return 3;
    else if(c=='+') return 2;
    else if(c=='>') return 1;
    else if(c=='~') return 0;
    else if (c=='(') return -1;
    else return -2;
}

void dfs(int u)
{
    if(u == n_logic)
    {
        vector<char> cya = a_logic;
        vector<int> cyay = ay;
        for(size_t i=0; i<a_logic.size(); i++)
        {
            if(((cya[i]>='A' && cya[i]<='Z')||(cya[i]>='a' && cya[i]<='z'))&& cya[i]!='T' && cya[i]!='F') {
                int idx=mirror[cya[i]];
                calc.push_back(cyay[idx]);
            }
            else if(cya[i]=='!') {
                x=calc.back(); calc.pop_back();
                x=no(x); calc.push_back(x);
            }
            else if(cya[i]=='+') {
                y=calc.back(); calc.pop_back();
                x=calc.back(); calc.pop_back();
                calc.push_back(xiqu(x,y));
            }
            else if(cya[i]=='*') {
                y=calc.back(); calc.pop_back();
                x=calc.back(); calc.pop_back();
                calc.push_back(hequ(x,y));
            }
            else if(cya[i]=='>') {
                y=calc.back(); calc.pop_back();
                x=calc.back(); calc.pop_back();
                calc.push_back(yunhan(x,y));
            }
            else if(cya[i]=='~') {
                y=calc.back(); calc.pop_back();
                x=calc.back(); calc.pop_back();
                calc.push_back(dengjia(x,y));
            }
        }

        vector<int> row_result;
        for(size_t i=0; i<order.size(); i++) {
            row_result.push_back(ay[i]);
        }
        row_result.push_back(calc.back());
        table_data.push_back(row_result);

        calc.clear();
        cyay.clear();
        cya.clear();
        return ;
    }
    for(int i=0; i<=1; i++)
    {
        ay[u] = i;
        dfs(u+1);
    }
}

bool creat()
{
    for(auto i : s_logic)
    {
        if(i==' ') continue;
        else if(((i>='A' && i<='Z')||(i>='a'&&i<='z')) && i!='T' && i!='F')
            a_logic.push_back(i);
        else if(i=='(')
            b_logic.push_back(i);
        else if(i=='!'||i=='+'||i=='*'||i=='>'||i=='~')
        {
            if(b_logic.empty()) b_logic.push_back(i);
            else
            {
                while(!b_logic.empty() && value(b_logic.back()) >= value(i))
                {
                    a_logic.push_back(b_logic.back());
                    b_logic.pop_back();
                }
                b_logic.push_back(i);
            }
        }
        else if(i==')')
        {
            while(!b_logic.empty() && b_logic.back()!='(')
            {
                a_logic.push_back(b_logic.back());
                b_logic.pop_back();
            }
            if(!b_logic.empty()) b_logic.pop_back();
        }
        else
        {
            error_msg = QString("Unknown symbol: '%1'!").arg(i);
            return false;
        }
    }
    while(!b_logic.empty())
    {
        if (b_logic.back()=='(')
        {
            error_msg = "Error: Unmatched parentheses!";
            return false;
        }
        a_logic.push_back(b_logic.back());
        b_logic.pop_back();
    }

    for(char c : a_logic) {
        if ((((c>='A' && c<='Z')||(c>='a'&&c<='z')) && c!='T' && c!='F') && !unique_vars.count(c)) {
            unique_vars.insert(c);
            order.push_back(c);
        }
    }
    n_logic = order.size();
    for(int i=0; i<n_logic; ++i)
        mirror[order[i]] = i;

    return true;
}

void Widget::on_btn_calc_logic_clicked()
{
    a_logic.clear(); order.clear(); mirror.clear(); b_logic.clear();
    ay.clear(); calc.clear(); unique_vars.clear(); table_data.clear();
    n_logic = 0; error_msg = "";

    QString qStr = ui->lineEdit_logic->text().trimmed();
    if(qStr.isEmpty()) {
        QMessageBox::warning(this, "提示", "请输入公式！");
        return;
    }
    s_logic = qStr.toStdString();

    if (!creat()) {
        QMessageBox::critical(this, "错误", error_msg);
        return;
    }

    if (n_logic == 0) {
        QMessageBox::warning(this, "提示", "未找到有效的变元！");
        return;
    }

    ay.resize(n_logic);
    dfs(0);

    ui->tableWidget_logic->clear();
    ui->tableWidget_logic->setColumnCount(n_logic + 1);
    ui->tableWidget_logic->setRowCount(table_data.size());

    QStringList headers;
    for(int i = 0; i < n_logic; ++i) {
        headers << QString(order[i]);
    }
    headers << "结果 (" + qStr + ")";
    ui->tableWidget_logic->setHorizontalHeaderLabels(headers);
    ui->tableWidget_logic->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);

    for(size_t row = 0; row < table_data.size(); ++row) {
        for(size_t col = 0; col < table_data[row].size(); ++col) {

            QTableWidgetItem* item = new QTableWidgetItem(QString::number(table_data[row][col]));
            item->setTextAlignment(Qt::AlignCenter);

            if (col == table_data[row].size() - 1) {
                QFont f; f.setBold(true); item->setFont(f);
                if (table_data[row][col] == 1) {
                    item->setForeground(QBrush(QColor(0, 150, 0)));
                } else {
                    item->setForeground(QBrush(Qt::red));
                }
            }
            ui->tableWidget_logic->setItem(row, col, item);
        }
    }
}
