import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from Connectors.Connector import Connector  # Import the updated Connector class

class ChartHandle:
    def __init__(self, df):
        self.df = df
    def showChartCreditScore(self, figure):
        figure.clf()  # Clear the figure to avoid overlapping plots
        credit_score = self.df['credit_score']
        sns.kdeplot(credit_score, fill=True, color='lightskyblue')
        plt.xlabel('Credit_Score',fontsize=8)
        plt.ylabel('Density',fontsize=8)
        plt.title('Credit Score Distribution (KDE)',fontsize=10)
        plt.tight_layout()

    def showChartCountry(self, figure):
        figure.clf()  # Clear the figure to avoid overlapping plots
        xcountry_counts = self.df['country'].value_counts()
        labels = xcountry_counts.index
        sizes = xcountry_counts.values
        colors = ['lightcoral', 'lightskyblue', 'lightyellow']

        bars = plt.barh(labels, sizes, color=colors)
        plt.xlabel('Frequency', fontsize=8)
        plt.title('Country Distribution', fontsize=10)
        plt.tight_layout()

        # Tăng giá trị trục x
        max_size = max(sizes) * 1.2  # Tăng thêm 20% giá trị lớn nhất
        plt.xlim(0, max_size)

        # Thêm nhãn cho từng thanh
        for bar in bars:
            width = bar.get_width()
            plt.text(width * 1.02, bar.get_y() + bar.get_height() / 2, '{}'.format(width), va='center',  ha='left', fontsize=8)

        plt.gca().invert_yaxis()  # Đảo ngược trục y để hiển thị nước giảm dần

    def showChartGender(self, figure):
        figure.clf()  # Xóa bảng để tránh trùng lặp các biểu đồ

        # Tính toán số lượng khách hàng theo các nhóm churn và giới tính
        churn_gender_counts = self.df.groupby(['churn', 'gender']).size().unstack(fill_value=0)

        # Tạo biểu đồ
        labels = ['Male', 'Female']
        stayed_counts = [churn_gender_counts.loc[0, 'Male'], churn_gender_counts.loc[0, 'Female']]
        exited_counts = [churn_gender_counts.loc[1, 'Male'], churn_gender_counts.loc[1, 'Female']]

        x = range(len(labels))
        width = 0.35

        # Vẽ biểu đồ
        plt.bar(x, stayed_counts, width, label='Stayed', color='lightskyblue')
        plt.bar([p + width for p in x], exited_counts, width, label='Exited', color='lightcoral')

        plt.ylabel('Frequency', fontsize=8)
        plt.title('Churn by Gender', fontsize=10)
        plt.xticks([p + width / 2 for p in x], labels, fontsize=8)
        plt.legend()

        # Thêm nhãn cho từng cột
        self.autolabel(plt.gca())

        # Tăng giá trị trên trục y
        max_y = max(stayed_counts + exited_counts) * 1.2  # Tăng thêm 20% giá trị lớn nhất
        plt.ylim(0, max_y)

        plt.tight_layout()

    def showChartAge(self, figure):
        figure.clf()  # Clear the figure to avoid overlapping plots
        ages = self.df['age']
        plt.hist(ages, bins=30, color='lightskyblue', edgecolor='blue')
        plt.xlabel('Age',fontsize=8)
        plt.ylabel('Frequency',fontsize=8)
        plt.title('Age Distribution',fontsize=10)
        plt.tight_layout()

    def showChartTenure(self, figure):
        figure.clf()  # Clear the figure to avoid overlapping plots
        xtenure_counts = self.df['tenure'].value_counts()
        labels = xtenure_counts.index
        sizes = xtenure_counts.values
        plt.bar(labels, sizes, color=['lightskyblue'])
        plt.xlabel('Tenure',fontsize=8)
        plt.ylabel('Frequency',fontsize=8)
        plt.title('Tenure Distribution',fontsize=10)
        plt.tight_layout()

        # Thêm nhãn cho từng cột
        self.autolabel(plt.gca())

        # Tăng giá trị trên trục y
        max_y = max(sizes) * 1.2  # Tăng thêm 20% giá trị lớn nhất
        plt.ylim(0, max_y)

    def showChartProduct(self, figure):
        figure.clf()  # Xóa bảng để tránh trùng lặp các biểu đồ

        # Tính toán số lượng khách hàng theo các nhóm churn và product number
        churn_product_number_counts = self.df.groupby(['churn', 'products_number']).size().unstack(fill_value=0)

        # Tạo biểu đồ
        product_labels = sorted(self.df['products_number'].unique())
        labels = [f'{label}' for label in product_labels]
        stayed_counts = [churn_product_number_counts.loc[0, label] for label in product_labels]
        exited_counts = [churn_product_number_counts.loc[1, label] for label in product_labels]

        x = range(len(labels))
        width = 0.35

        # Vẽ biểu đồ
        plt.bar(x, stayed_counts, width, label='Stayed', color='lightskyblue')
        plt.bar([p + width for p in x], exited_counts, width, label='Exited', color='lightcoral')

        plt.ylabel('Frequency', fontsize=8)
        plt.title('Churn by Product Number', fontsize=10)
        plt.xticks([p + width / 2 for p in x], labels, fontsize=8)
        plt.legend()

        # Thêm nhãn cho từng cột
        self.autolabel(plt.gca())

        # Tăng giá trị trên trục y
        max_y = max(stayed_counts + exited_counts) * 1.2  # Tăng thêm 20% giá trị lớn nhất
        plt.ylim(0, max_y)

        plt.tight_layout()

    def showChartActive(self, figure):
        figure.clf()  # Xóa bảng để tránh trùng lặp các biểu đồ

        # Tính toán số lượng khách hàng theo các nhóm churn và active member
        churn_active_member_counts = self.df.groupby(['churn', 'active_member']).size().unstack(fill_value=0)

        # Tạo biểu đồ
        labels = ['Active Member', 'Inactive Member', 'Active Member', 'Inactive Member']
        stayed_active = churn_active_member_counts.loc[0, 1]
        stayed_inactive = churn_active_member_counts.loc[0, 0]
        exited_active = churn_active_member_counts.loc[1, 1]
        exited_inactive = churn_active_member_counts.loc[1, 0]

        x = range(len(labels))
        width = 0.35

        # Vẽ biểu đồ
        plt.bar(x[:2], [stayed_active, stayed_inactive], width, label='Stayed', color='lightskyblue')
        plt.bar(x[2:], [exited_active, exited_inactive], width, label='Exited', color='lightcoral')

        plt.ylabel('Frequency', fontsize=8)
        plt.title('Churn by Active Member', fontsize=10)
        plt.xticks(x, labels, fontsize=8)
        plt.legend()

        # Thêm nhãn cho từng cột
        self.autolabel(plt.gca())

        # Tăng giá trị trên trục y
        max_y = max(stayed_active, stayed_inactive, exited_active,
                    exited_inactive) * 1.2  # Tăng thêm 20% giá trị lớn nhất
        plt.ylim(0, max_y)

        plt.tight_layout()

    def showChartChurn(self, figure):
        figure.clf()  # Clear the figure to avoid overlapping plots
        xchurn_counts = self.df['churn'].value_counts()
        labels = ['Churn', 'No Churn']
        sizes = [xchurn_counts[1], xchurn_counts[0]]
        colors = ['lightcoral', 'lightskyblue']

        plt.suptitle('Churn Distribution', fontsize=10)

        plt.subplot(1, 2, 1)
        bar_width = 0.5  # Adjust this value to change the width of the bars
        rects = plt.bar(labels, sizes, color=colors, width=bar_width)
        plt.ylabel('Frequency', fontsize=8)

        # Tăng giá trị trên trục y
        max_y = max(sizes) * 1.2  # Tăng thêm 20% giá trị lớn nhất
        plt.ylim(0, max_y)

        self.autolabel(plt.gca())

        plt.subplot(1, 2, 2)
        explode = (0.1, 0)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 8})
        plt.axis('equal')
        plt.tight_layout()

    def showChartCreditCard(self, figure):
        figure.clf()  # Xóa bảng để tránh trùng lặp các biểu đồ

        # Tính toán số lượng khách hàng theo các nhóm churn và credit card
        churn_credit_card_counts = self.df.groupby(['churn', 'credit_card']).size().unstack(fill_value=0)

        # Tạo biểu đồ
        labels = ['Has Credit Card', 'No Credit Card', 'Has Credit Card', 'No Credit Card']
        stayed_has_cc = churn_credit_card_counts.loc[0, 1]
        stayed_no_cc = churn_credit_card_counts.loc[0, 0]
        exited_has_cc = churn_credit_card_counts.loc[1, 1]
        exited_no_cc = churn_credit_card_counts.loc[1, 0]

        x = range(len(labels))
        width = 0.35

        # Vẽ biểu đồ
        plt.bar(x[:2], [stayed_has_cc, stayed_no_cc], width, label='Stayed', color='lightskyblue')
        plt.bar(x[2:], [exited_has_cc, exited_no_cc], width, label='Exited', color='lightcoral')

        plt.ylabel('Frequency', fontsize=8)
        plt.title('Churn by Credit Card', fontsize=10)
        plt.xticks(x, labels, fontsize=8)
        plt.legend()

        # Thêm nhãn cho từng cột
        self.autolabel(plt.gca())

        # Tăng giá trị trên trục y
        max_y = max(stayed_has_cc, stayed_no_cc, exited_has_cc, exited_no_cc) * 1.2  # Tăng thêm 20% giá trị lớn nhất
        plt.ylim(0, max_y)

        plt.tight_layout()

    def autolabel(self, ax):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in ax.patches:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')