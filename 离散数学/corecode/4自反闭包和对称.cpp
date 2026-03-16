#include<bits/stdc++.h>
using namespace std;
using mat=vector<vector<char>>;
using clk=chrono::high_resolution_clock;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    size_t n,m;
    cout<<"Please input SET size:"<<endl;
    cout<<"n="<<flush;
    if(!(cin>>n))
	  return 1;
    cout<<"m="<<flush;
    if(!(cin>>m))
	  return 1;
    mat a(n,vector<char>(n,0));
    mt19937_64 r(chrono::steady_clock::now().time_since_epoch().count());
    uniform_int_distribution<size_t>d(0,n-1);
    for(size_t k=0;k<m;++k) 
	  a[d(r)][d(r)]=1;
    mat b(n,vector<char>(n,0)),c(n,vector<char>(n,0));
    size_t ci=0,cv=0;
    for(size_t i=0;i<n;++i)
	{
		b[i][i]=1;
		++ci;
	}
    for(size_t i=0;i<n;++i)for(size_t j=0;j<n;++j)if(a[i][j]&&!c[j][i])
	{
		c[j][i]=1;
		++cv;
	}
    cout<<fixed<<setprecision(15);
    const int t=1000;
    double tr=0,ts=0;
    for(int x=0;x<t;++x)
	{
        mat rr=a;
		auto s=clk::now();
        for(size_t i=0;i<n;++i)
		  rr[i][i]=1;
        auto e=clk::now();
		tr+=chrono::duration<double>(e-s).count();
    }
    cout<<"O(Reflexive R) avg over"<<t<<"="<<(tr/t)<<"s"<<endl;
    for(int x=0;x<t;++x)
	{
        mat rs(n,vector<char>(n,0));auto s=clk::now();
        for(size_t i=0;i<n;++i)
		{
		  for(size_t j=0;j<n;++j)
		  {
		  	if(a[i][j])
			  rs[i][j]=rs[j][i]=1;	
		  }
		}
        auto e=clk::now();
		ts+=chrono::duration<double>(e-s).count();
    }
    cout<<"O(Symmetric R) avg over"<<t<<"="<<(ts/t)<<"s"<<endl;
    return 0;
}
