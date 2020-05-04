library(utils) # 為了讀csv
Audi_data = read.csv('/Users/lijicheng/Downloads/履歷表/奧迪福斯資料分析/result.csv')
Audi_data_summary = summary(Audi_data) # 基本資料
library(magrittr) # 才能用 %>%
library(dplyr) # 才能用mutate()

attach(Audi_data) # 為了讓系統讀得到Audi_data中的每一行標題
Audi_data <- Audi_data %>%
  mutate( Depreciation_percentage = 100 * (Original.Price.NT.. - Secondhand.Price.NT..)/Original.Price.NT.. ) 
# 新增折舊率
Rl_2v = lm( Depreciation_percentage ~  Days + Mileage.km. ) # 2個自變數的複回歸
Rl_Days = lm( Depreciation_percentage ~  Days ) # 自變數為天數的簡單迴歸
Rl_Mileage = lm( Depreciation_percentage ~  Mileage.km. ) # 自變數為里程數的簡單迴歸
anova(Rl_Days,Rl_2v) # p-value > 0.05，不能拒絕虛無假設，只有車齡為自變數的模型較好
anova(Rl_Mileage,Rl_2v) # p-value < 0.05，拒絕虛無假設，full model較只有里程數為自變數的模型好
# 模型優劣比較： 車齡為自變數 > full model > 里程數為自變數 
Rl_Days_summary = summary(Rl_Days) # p-value < 0.05，拒絕虛無假設，迴歸係數顯著
# 註：簡單迴歸中，f-test和t-test意義相同，因此不用再做t-test

library(ggplot2) # 載入畫圖套件
ggplot(Audi_data, aes(Days,Depreciation_percentage))+ # x軸為車齡，y軸為折舊比率
   geom_smooth(method="lm") + # 畫出回歸線
   geom_line()+ # 點與點之間以直線連接
   geom_point() # 標出各點

#畫出回歸線後，可看到有些許殘差較大的離群值。
#但除了車齡以外，還有其他與車況相關之因素會影響折舊率，因此判斷這些離群值係屬正常，不予以刪除

# 建立迴歸模型時，必須確認其殘差(residual)符合三個假設： 1.常態性假設 2.獨立性假設 3.同質性假設
shapiro.test(Rl_Days$residual) # 檢驗常態性假設
# 虛無假設H0:殘差服從常態分配，因為p-value < 0.05，拒絕H0，推論殘差不服從常態分配
# 殘差的常態假設並非必要，通常是較大的樣本（300~500）才會服從，一般來說以最小平方法建立回歸模型時無須符合
# 若要做進一步檢定才必須符合
require(car) # 載入套件（為了檢驗獨立性與同質性）
durbinWatsonTest(Rl_Days) # 檢驗獨立性假設
# 虛無假設H0:殘差間相互獨立，因為p-value > 0.05，不拒絕H0，推論殘差間相互獨立
ncvTest(Rl_Days)
# 虛無假設H0:殘差變異數具有同質性，因為p-value > 0.05，不拒絕H0，推論殘差變異數具有同質性
# 三項假設均符合，迴歸模型可以使用

