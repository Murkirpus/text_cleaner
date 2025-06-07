import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import unicodedata
import re

class NonStandardCharHighlighter:
    def __init__(self, root):
        self.root = root
        self.root.title("Блокнот с подсветкой нестандартных символов")
        self.root.geometry("900x700")
        
        # Определяем стандартные символы
        self.define_standard_chars()
        
        # Настраиваем теги для подсветки
        self.setup_highlight_tags()
        
        # Создаем меню
        self.create_menu()
        
        # Создаем панель инструментов
        self.create_toolbar()
        
        # Создаем основное окно с текстом
        self.create_text_widget()
        
        # Создаем контекстное меню
        self.create_context_menu()
        
        # Создаем панель информации
        self.create_info_panel()
        
        # Привязываем события
        self.bind_events()
    
    def define_standard_chars(self):
        """Определяем множество стандартных символов"""
        self.standard_chars = set()
        
        # Обычные ASCII символы (32-126)
        for i in range(32, 127):
            self.standard_chars.add(chr(i))
        
        # Стандартные управляющие символы
        self.standard_chars.update(['\n', '\t', '\r'])
        
        # Кириллические символы
        for i in range(0x0400, 0x04FF + 1):
            try:
                char = chr(i)
                if unicodedata.category(char) in ['Lu', 'Ll', 'Lo']:  # Буквы
                    self.standard_chars.add(char)
            except:
                pass
        
        # Дополнительные символы кириллицы
        additional_cyrillic = "ёЁәғқңөұүһІі"
        self.standard_chars.update(additional_cyrillic)
        
        # Стандартные знаки препинания и символы
        punctuation = ".,;:!?()[]{}\"'«»—–-+=*/#@$%^&|\\`~№"
        self.standard_chars.update(punctuation)
        
        # Цифры и математические символы
        digits_math = "0123456789<>≤≥≠±×÷√∞"
        self.standard_chars.update(digits_math)
    
    def setup_highlight_tags(self):
        """Настраиваем теги для подсветки разных типов символов"""
        # Будет переопределено после создания text_widget
        pass
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню "Правка"
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Найти нестандартные символы", command=self.highlight_all)
        edit_menu.add_command(label="Очистить подсветку", command=self.clear_highlights)
        edit_menu.add_separator()
        edit_menu.add_command(label="Заменить нестандартные пробелы", command=self.replace_spaces)
        edit_menu.add_command(label="Заменить ВСЕ подозрительные символы", command=self.replace_all_suspicious)
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        ttk.Button(toolbar, text="Подсветить", command=self.highlight_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Очистить", command=self.clear_highlights).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Заменить пробелы", command=self.replace_spaces).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Исправить ВСЕ", command=self.replace_all_suspicious).pack(side=tk.LEFT, padx=2)
        
        # Чекбокс для автоподсветки
        self.auto_highlight = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text="Автоподсветка", variable=self.auto_highlight).pack(side=tk.LEFT, padx=10)
    
    def create_text_widget(self):
        # Создаем фрейм для текста
        text_frame = ttk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Текстовое поле с прокруткой
        self.text_widget = scrolledtext.ScrolledText(
            text_frame, 
            wrap=tk.WORD, 
            font=("Consolas", 12),
            undo=True
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Настраиваем теги для подсветки после создания виджета
        self.setup_highlight_tags_real()
    
    def setup_highlight_tags_real(self):
        """Настраиваем теги для подсветки разных типов символов"""
        # Невидимые символы - красный фон
        self.text_widget.tag_config("invisible", background="#ffcccc", relief="raised")
        
        # Похожие символы - желтый фон
        self.text_widget.tag_config("similar", background="#ffffcc", relief="raised")
        
        # Специальные пробелы - голубой фон
        self.text_widget.tag_config("space", background="#ccffff", relief="raised")
        
        # Управляющие символы - розовый фон
        self.text_widget.tag_config("control", background="#ffccff", relief="raised")
    
    def create_context_menu(self):
        """Создаем контекстное меню для правой кнопки мыши"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        
        # Стандартные операции
        self.context_menu.add_command(label="Вырезать", command=self.cut_text, accelerator="Ctrl+X")
        self.context_menu.add_command(label="Копировать", command=self.copy_text, accelerator="Ctrl+C")
        self.context_menu.add_command(label="Вставить", command=self.paste_text, accelerator="Ctrl+V")
        self.context_menu.add_separator()
        
        # Операции с выделением
        self.context_menu.add_command(label="Выделить все", command=self.select_all_text, accelerator="Ctrl+A")
        self.context_menu.add_separator()
        
        # Специальные функции
        self.context_menu.add_command(label="🔍 Подсветить нестандартные символы", command=self.highlight_all)
        self.context_menu.add_command(label="🧹 Очистить подсветку", command=self.clear_highlights)
        self.context_menu.add_separator()
        
        # Функции исправления
        self.context_menu.add_command(label="🔧 Исправить ВСЕ подозрительные символы", command=self.replace_all_suspicious)
        self.context_menu.add_command(label="📏 Заменить только пробелы", command=self.replace_spaces)
        self.context_menu.add_separator()
        
        # Анализ выделенного текста
        self.context_menu.add_command(label="📊 Анализ выделенного текста", command=self.analyze_selection)
        self.context_menu.add_command(label="🔧 Исправить только выделенное", command=self.fix_selection)
    
    def create_info_panel(self):
        info_frame = ttk.Frame(self.root)
        info_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов")
        self.status_label = ttk.Label(info_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT)
        
        # Информация о символе под курсором
        self.char_info_var = tk.StringVar(value="")
        self.char_info_label = ttk.Label(info_frame, textvariable=self.char_info_var)
        self.char_info_label.pack(side=tk.RIGHT)
    
    def bind_events(self):
        """Привязываем события"""
        # Горячие клавиши
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        
        # Событие изменения текста
        self.text_widget.bind('<KeyRelease>', self.on_text_change)
        self.text_widget.bind('<Button-1>', self.on_cursor_move)
        self.text_widget.bind('<ButtonRelease-1>', self.on_cursor_move)
        self.text_widget.bind('<Key>', self.on_cursor_move)
        
        # Контекстное меню
        self.text_widget.bind('<Button-3>', self.show_context_menu)  # Правая кнопка мыши
        
        # Дополнительные горячие клавиши
        self.root.bind('<Control-x>', lambda e: self.cut_text())
        self.root.bind('<Control-c>', lambda e: self.copy_text())
        self.root.bind('<Control-v>', lambda e: self.paste_text())
        self.root.bind('<Control-a>', lambda e: self.select_all_text())
    
    def on_text_change(self, event=None):
        """Обработчик изменения текста"""
        if self.auto_highlight.get():
            self.root.after(100, self.highlight_all)  # Задержка для производительности
        self.update_char_info()
    
    def on_cursor_move(self, event=None):
        """Обработчик движения курсора"""
        self.root.after(10, self.update_char_info)
    
    def update_char_info(self):
        """Обновляем информацию о символе под курсором"""
        try:
            cursor_pos = self.text_widget.index(tk.INSERT)
            char = self.text_widget.get(cursor_pos)
            
            if char:
                char_info = self.get_char_info(char)
                self.char_info_var.set(char_info)
            else:
                self.char_info_var.set("")
        except:
            self.char_info_var.set("")
    
    def get_char_info(self, char):
        """Получаем информацию о символе"""
        try:
            unicode_point = ord(char)
            unicode_name = unicodedata.name(char, f"U+{unicode_point:04X}")
            category = unicodedata.category(char)
            
            info = f"'{char}' U+{unicode_point:04X} ({unicode_name}) [{category}]"
            
            if char not in self.standard_chars:
                info += " [НЕСТАНДАРТНЫЙ]"
            
            return info
        except:
            return ""
    
    def highlight_all(self):
        """Подсвечиваем все нестандартные символы"""
        self.clear_highlights()
        
        text = self.text_widget.get("1.0", tk.END)
        non_standard_count = 0
        
        for i, char in enumerate(text):
            if char not in self.standard_chars and char != '\n':  # Исключаем символ конца файла
                line_col = f"1.0+{i}c"
                end_pos = f"1.0+{i+1}c"
                
                # Определяем тип символа и применяем соответствующую подсветку
                if self.is_invisible_char(char):
                    self.text_widget.tag_add("invisible", line_col, end_pos)
                elif self.is_special_space(char):
                    self.text_widget.tag_add("space", line_col, end_pos)
                elif self.is_similar_char(char):
                    self.text_widget.tag_add("similar", line_col, end_pos)
                else:
                    self.text_widget.tag_add("control", line_col, end_pos)
                
                non_standard_count += 1
        
        self.status_var.set(f"Найдено нестандартных символов: {non_standard_count}")
    
    def clear_highlights(self):
        """Очищаем всю подсветку"""
        for tag in ["invisible", "similar", "space", "control"]:
            self.text_widget.tag_remove(tag, "1.0", tk.END)
        self.status_var.set("Подсветка очищена")
    
    def replace_spaces(self):
        """Заменяем нестандартные пробелы на обычные"""
        text = self.text_widget.get("1.0", tk.END)
        
        # Заменяем все виды нестандартных пробелов на обычный пробел
        space_chars = [
            '\u00a0', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005',
            '\u2006', '\u2007', '\u2008', '\u2009', '\u200a', '\u202f', '\u205f', '\u3000'
        ]
        
        original_text = text
        for space_char in space_chars:
            text = text.replace(space_char, ' ')
        
        if text != original_text:
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", text)
            self.status_var.set("Нестандартные пробелы заменены на обычные")
            if self.auto_highlight.get():
                self.highlight_all()
        else:
            self.status_var.set("Нестандартные пробелы не найдены")
    
    def replace_all_suspicious(self):
        """Заменяем ВСЕ подозрительные символы на нормальные аналоги"""
        text = self.text_widget.get("1.0", tk.END)
        original_text = text
        replacements_count = 0
        
        # Словарь замен для похожих символов
        similar_replacements = {
            # Кириллические буквы, похожие на латинские
            'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
            'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 
            'Р': 'P', 'С': 'C', 'Т': 'T', 'У': 'Y', 'Х': 'X',
            
            # Специальные кавычки и тире
            '"': '"', '"': '"', ''': "'", ''': "'", '‚': ',', '„': '"',
            '‹': '<', '›': '>', '«': '"', '»': '"',
            '—': '-', '–': '-', '−': '-', '‒': '-', '―': '-',
            
            # Специальные символы
            '…': '...', '№': 'No.', '§': 'S', '¶': 'P',
            '©': '(c)', '®': '(r)', '™': '(tm)', '℠': '(sm)',
            '°': 'deg', '±': '+/-', '×': 'x', '÷': '/', '·': '*',
            '‰': '%', '‱': '%', '℃': 'C', '℉': 'F',
            
            # Дроби
            '½': '1/2', '⅓': '1/3', '¼': '1/4', '¾': '3/4', '⅕': '1/5',
            '⅖': '2/5', '⅗': '3/5', '⅘': '4/5', '⅙': '1/6', '⅚': '5/6',
            '⅛': '1/8', '⅜': '3/8', '⅝': '5/8', '⅞': '7/8', '⅐': '1/7',
            '⅑': '1/9', '⅒': '1/10',
            
            # Надстрочные и подстрочные цифры
            '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5',
            '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
            '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5',
            '₆': '6', '₇': '7', '₈': '8', '₉': '9',
            
            # Стрелки
            '→': '->', '←': '<-', '↑': '^', '↓': 'v', '↕': '<->',
            '⇒': '=>', '⇐': '<=', '↔': '<->', '⇔': '<=>', 
            '⟵': '<-', '⟶': '->', '⟷': '<->', '⟸': '<=', '⟹': '=>',
            '↗': '^>', '↘': 'v>', '↙': '<v', '↖': '<^',
            '➡': '->', '⬅': '<-', '⬆': '^', '⬇': 'v',
            
            # Математические символы
            '≤': '<=', '≥': '>=', '≠': '!=', '≈': '~=', '≡': '===',
            '∞': 'inf', '√': 'sqrt', '∑': 'sum', '∏': 'prod',
            '∫': 'integral', '∂': 'd', '∆': 'delta', '∇': 'nabla',
            '∈': 'in', '∉': 'not in', '∋': 'contains', '⊂': 'subset',
            '⊃': 'superset', '⊆': 'subseteq', '⊇': 'superseteq',
            '∪': 'union', '∩': 'intersect', '∅': 'empty',
            '⊕': 'xor', '⊗': 'tensor', '⊙': 'dot',
            '∧': 'and', '∨': 'or', '¬': 'not', '∀': 'forall', '∃': 'exists',
            
            # Греческие буквы
            'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'ε': 'epsilon',
            'ζ': 'zeta', 'η': 'eta', 'θ': 'theta', 'ι': 'iota', 'κ': 'kappa',
            'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
            'π': 'pi', 'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon',
            'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega',
            'Α': 'Alpha', 'Β': 'Beta', 'Γ': 'Gamma', 'Δ': 'Delta', 'Ε': 'Epsilon',
            'Ζ': 'Zeta', 'Η': 'Eta', 'Θ': 'Theta', 'Ι': 'Iota', 'Κ': 'Kappa',
            'Λ': 'Lambda', 'Μ': 'Mu', 'Ν': 'Nu', 'Ξ': 'Xi', 'Ο': 'Omicron',
            'Π': 'Pi', 'Ρ': 'Rho', 'Σ': 'Sigma', 'Τ': 'Tau', 'Υ': 'Upsilon',
            'Φ': 'Phi', 'Χ': 'Chi', 'Ψ': 'Psi', 'Ω': 'Omega',
            
            # Символы валют
            '€': 'EUR', '£': 'GBP', '¥': 'JPY', '¢': 'cent', '₽': 'RUB',
            '₴': 'UAH', '₨': 'Rs', '₹': 'Rs', '₩': 'Won', '₪': 'NIS',
            
            # Дополнительные символы
            '☑': '[x]', '☐': '[ ]', '✓': 'v', '✗': 'x', '✘': 'x',
            '★': '*', '☆': '*', '♦': 'diamond', '♠': 'spade',
            '♣': 'club', '♥': 'heart', '♪': 'note', '♫': 'notes',
            '†': '+', '‡': '++', '•': '*', '◦': 'o', '‣': '>',
            '▪': '*', '▫': 'o', '▲': '^', '▼': 'v', '◄': '<', '►': '>',
            '∙': '*', '∘': 'o', '⋅': '*', '⋆': '*', '⋄': 'diamond',
            
            # Римские цифры
            'Ⅰ': 'I', 'Ⅱ': 'II', 'Ⅲ': 'III', 'Ⅳ': 'IV', 'Ⅴ': 'V',
            'Ⅵ': 'VI', 'Ⅶ': 'VII', 'Ⅷ': 'VIII', 'Ⅸ': 'IX', 'Ⅹ': 'X',
            'ⅰ': 'i', 'ⅱ': 'ii', 'ⅲ': 'iii', 'ⅳ': 'iv', 'ⅴ': 'v',
            'ⅵ': 'vi', 'ⅶ': 'vii', 'ⅷ': 'viii', 'ⅸ': 'ix', 'ⅹ': 'x',
        }
        
        # Заменяем похожие символы
        for suspicious, normal in similar_replacements.items():
            if suspicious in text:
                count = text.count(suspicious)
                text = text.replace(suspicious, normal)
                replacements_count += count
        
        # Заменяем все виды нестандартных пробелов на обычный пробел
        space_chars = [
            '\u00a0',  # Non-breaking space
            '\u2000',  # En quad
            '\u2001',  # Em quad
            '\u2002',  # En space
            '\u2003',  # Em space
            '\u2004',  # Three-per-em space
            '\u2005',  # Four-per-em space
            '\u2006',  # Six-per-em space
            '\u2007',  # Figure space
            '\u2008',  # Punctuation space
            '\u2009',  # Thin space
            '\u200a',  # Hair space
            '\u202f',  # Narrow no-break space
            '\u205f',  # Medium mathematical space
            '\u3000',  # Ideographic space
        ]
        
        for space_char in space_chars:
            if space_char in text:
                count = text.count(space_char)
                text = text.replace(space_char, ' ')
                replacements_count += count
        
        # Удаляем невидимые символы
        invisible_chars = [
            '\u200b',  # Zero width space
            '\u200c',  # Zero width non-joiner
            '\u200d',  # Zero width joiner
            '\u2060',  # Word joiner
            '\ufeff',  # Byte order mark
            '\u00ad',  # Soft hyphen
            '\u034f',  # Combining grapheme joiner
            '\u061c',  # Arabic letter mark
            '\u115f',  # Hangul choseong filler
            '\u1160',  # Hangul jungseong filler
            '\u17b4',  # Khmer vowel inherent AQ
            '\u17b5',  # Khmer vowel inherent AA
            '\u180e',  # Mongolian vowel separator
            '\u2028',  # Line separator
            '\u2029',  # Paragraph separator
            '\u202a',  # Left-to-right embedding
            '\u202b',  # Right-to-left embedding
            '\u202c',  # Pop directional formatting
            '\u202d',  # Left-to-right override
            '\u202e',  # Right-to-left override
            '\u2061',  # Function application
            '\u2062',  # Invisible times
            '\u2063',  # Invisible separator
            '\u2064',  # Invisible plus
            '\u206a',  # Inhibit symmetric swapping
            '\u206b',  # Activate symmetric swapping
            '\u206c',  # Inhibit arabic form shaping
            '\u206d',  # Activate arabic form shaping
            '\u206e',  # National digit shapes
            '\u206f',  # Nominal digit shapes
            '\uffa0',  # Halfwidth hangul filler
        ]
        
        for invisible_char in invisible_chars:
            if invisible_char in text:
                count = text.count(invisible_char)
                text = text.replace(invisible_char, '')
                replacements_count += count
        
        # Удаляем или заменяем другие проблемные символы
        other_problematic = {
            '\u00a1': '!',     # Inverted exclamation mark
            '\u00bf': '?',     # Inverted question mark
            '\u00b0': 'deg',   # Degree symbol
            '\u00b1': '+/-',   # Plus-minus sign
            '\u00b2': '2',     # Superscript two
            '\u00b3': '3',     # Superscript three
            '\u00b5': 'u',     # Micro sign
            '\u00b6': 'P',     # Pilcrow sign
            '\u00b7': '*',     # Middle dot
            '\u00b8': ',',     # Cedilla
            '\u00b9': '1',     # Superscript one
            '\u00ba': 'o',     # Masculine ordinal indicator
            '\u00bb': '>>',    # Right-pointing double angle quotation mark
            '\u00bc': '1/4',   # Vulgar fraction one quarter
            '\u00bd': '1/2',   # Vulgar fraction one half
            '\u00be': '3/4',   # Vulgar fraction three quarters
        }
        
        for problematic, replacement in other_problematic.items():
            if problematic in text:
                count = text.count(problematic)
                text = text.replace(problematic, replacement)
                replacements_count += count
        
        # Заменяем множественные пробелы на одинарные
        text = re.sub(r' +', ' ', text)
        
        # Убираем пробелы в начале и конце строк
        lines = text.split('\n')
        text = '\n'.join(line.strip() for line in lines)
        
        # Применяем изменения, если они есть
        if text != original_text:
            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", text)
            self.status_var.set(f"Исправлено символов: {replacements_count}")
            if self.auto_highlight.get():
                self.root.after(100, self.highlight_all)
        else:
            self.status_var.set("Подозрительные символы не найдены")
    
    def show_about(self):
        """Показываем информацию о программе"""
        about_text = """Блокнот с подсветкой нестандартных символов
        
Версия: 1.0

Программа предназначена для обнаружения и замены нестандартных символов в тексте, 
которые часто появляются после копирования из ChatGPT и других источников.

Возможности:
• Подсветка невидимых и похожих символов
• Автоматическая замена на стандартные аналоги
• Анализ выделенного текста
• Работа с файлами

Автор: Литвинов Виталий
Email: murkir@gmail.com

© 2025 Все права защищены"""

        # Создаем окно "О программе"
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("450x350")
        about_window.resizable(False, False)
        
        # Центрируем окно относительно главного окна
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Основной фрейм
        main_frame = ttk.Frame(about_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(
            main_frame, 
            text="Блокнот с подсветкой нестандартных символов",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Текст информации
        info_text = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            height=12,
            width=50,
            relief="flat",
            bg=about_window.cget("bg"),
            state=tk.DISABLED
        )
        info_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Вставляем текст
        info_text.config(state=tk.NORMAL)
        info_text.insert("1.0", about_text)
        info_text.config(state=tk.DISABLED)
        
        # Кнопка закрытия
        close_button = ttk.Button(
            main_frame,
            text="Закрыть",
            command=about_window.destroy
        )
        close_button.pack()
        
        # Фокус на кнопку
        close_button.focus()
    
    def show_context_menu(self, event):
        """Показываем контекстное меню"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def cut_text(self):
        """Вырезаем выделенный текст"""
        try:
            if self.text_widget.selection_get():
                self.text_widget.event_generate('<<Cut>>')
        except tk.TclError:
            pass  # Нет выделенного текста
    
    def copy_text(self):
        """Копируем выделенный текст"""
        try:
            if self.text_widget.selection_get():
                self.text_widget.event_generate('<<Copy>>')
        except tk.TclError:
            pass  # Нет выделенного текста
    
    def paste_text(self):
        """Вставляем текст из буфера обмена"""
        try:
            self.text_widget.event_generate('<<Paste>>')
            if self.auto_highlight.get():
                self.root.after(100, self.highlight_all)
        except tk.TclError:
            pass
    
    def select_all_text(self):
        """Выделяем весь текст"""
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.text_widget.mark_set(tk.INSERT, "1.0")
        self.text_widget.see(tk.INSERT)
    
    def analyze_selection(self):
        """Анализируем выделенный текст"""
        try:
            selected_text = self.text_widget.selection_get()
            if not selected_text:
                messagebox.showinfo("Анализ", "Текст не выделен")
                return
            
            # Анализируем символы
            total_chars = len(selected_text)
            non_standard_chars = []
            invisible_chars = []
            special_spaces = []
            similar_chars = []
            
            for i, char in enumerate(selected_text):
                if char not in self.standard_chars and char != '\n':
                    char_info = f"'{char}' (U+{ord(char):04X})"
                    non_standard_chars.append(char_info)
                    
                    if self.is_invisible_char(char):
                        invisible_chars.append(char_info)
                    elif self.is_special_space(char):
                        special_spaces.append(char_info)
                    elif self.is_similar_char(char):
                        similar_chars.append(char_info)
            
            # Формируем отчет
            report = f"Анализ выделенного текста:\n\n"
            report += f"Всего символов: {total_chars}\n"
            report += f"Нестандартных символов: {len(non_standard_chars)}\n\n"
            
            if invisible_chars:
                report += f"Невидимые символы ({len(invisible_chars)}):\n"
                for char in invisible_chars[:10]:  # Показываем максимум 10
                    report += f"  • {char}\n"
                if len(invisible_chars) > 10:
                    report += f"  ... и еще {len(invisible_chars) - 10}\n"
                report += "\n"
            
            if special_spaces:
                report += f"Специальные пробелы ({len(special_spaces)}):\n"
                for char in special_spaces[:10]:
                    report += f"  • {char}\n"
                if len(special_spaces) > 10:
                    report += f"  ... и еще {len(special_spaces) - 10}\n"
                report += "\n"
            
            if similar_chars:
                report += f"Похожие символы ({len(similar_chars)}):\n"
                for char in similar_chars[:10]:
                    report += f"  • {char}\n"
                if len(similar_chars) > 10:
                    report += f"  ... и еще {len(similar_chars) - 10}\n"
                report += "\n"
            
            if not non_standard_chars:
                report += "✅ Все символы стандартные!"
            
            # Показываем в отдельном окне
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("Анализ выделенного текста")
            analysis_window.geometry("500x400")
            
            text_area = scrolledtext.ScrolledText(analysis_window, wrap=tk.WORD, font=("Consolas", 10))
            text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_area.insert("1.0", report)
            text_area.config(state=tk.DISABLED)
            
        except tk.TclError:
            messagebox.showinfo("Анализ", "Текст не выделен")
    
    def fix_selection(self):
        """Исправляем только выделенный текст"""
        try:
            selected_text = self.text_widget.selection_get()
            if not selected_text:
                messagebox.showinfo("Исправление", "Текст не выделен")
                return
            
            # Получаем позицию выделения
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            # Применяем исправления только к выделенному тексту
            fixed_text = self.fix_text(selected_text)
            
            if fixed_text != selected_text:
                # Заменяем выделенный текст на исправленный
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, fixed_text)
                
                # Выделяем исправленный текст
                new_end = f"{sel_start}+{len(fixed_text)}c"
                self.text_widget.tag_add(tk.SEL, sel_start, new_end)
                
                self.status_var.set("Выделенный текст исправлен")
                if self.auto_highlight.get():
                    self.root.after(100, self.highlight_all)
            else:
                self.status_var.set("В выделенном тексте нет подозрительных символов")
                
        except tk.TclError:
            messagebox.showinfo("Исправление", "Текст не выделен")
    
    def fix_text(self, text):
        """Вспомогательная функция для исправления текста"""
        original_text = text
        
        # Словарь замен (сокращенная версия)
        similar_replacements = {
            'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
            'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 
            'Р': 'P', 'С': 'C', 'Т': 'T', 'У': 'Y', 'Х': 'X',
            '"': '"', '"': '"', ''': "'", ''': "'",
            '—': '-', '–': '-', '−': '-',
            '…': '...', '№': 'No.', '§': 'S',
            '©': '(c)', '®': '(r)', '™': '(tm)',
            '°': 'deg', '±': '+/-', '×': 'x', '÷': '/',
            '½': '1/2', '⅓': '1/3', '¼': '1/4', '¾': '3/4',
            '→': '->', '←': '<-', '↑': '^', '↓': 'v',
            '≤': '<=', '≥': '>=', '≠': '!=', '≈': '~=',
            'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'π': 'pi',
            '€': 'EUR', '£': 'GBP', '¥': 'JPY', '¢': 'cent',
            '★': '*', '☆': '*', '•': '*', '▪': '*', '∙': '*',
        }
        
        # Применяем замены
        for suspicious, normal in similar_replacements.items():
            text = text.replace(suspicious, normal)
        
        # Заменяем нестандартные пробелы
        space_chars = ['\u00a0', '\u2009', '\u202f', '\u2000', '\u2001', '\u2002', '\u2003']
        for space_char in space_chars:
            text = text.replace(space_char, ' ')
        
        # Удаляем невидимые символы
        invisible_chars = ['\u200b', '\u200c', '\u200d', '\ufeff', '\u00ad']
        for invisible_char in invisible_chars:
            text = text.replace(invisible_char, '')
        
        # Заменяем множественные пробелы
        text = re.sub(r' +', ' ', text)
        
        return text
    
    def is_invisible_char(self, char):
        """Проверяем, является ли символ невидимым"""
        invisible_chars = {
            '\u200b',  # Zero width space
            '\u200c',  # Zero width non-joiner
            '\u200d',  # Zero width joiner
            '\u2060',  # Word joiner
            '\ufeff',  # Byte order mark
            '\u00ad',  # Soft hyphen
        }
        return char in invisible_chars or unicodedata.category(char) in ['Cf', 'Mn']
    
    def is_special_space(self, char):
        """Проверяем, является ли символ специальным пробелом"""
        special_spaces = {
            '\u00a0',  # Non-breaking space
            '\u2000',  # En quad
            '\u2001',  # Em quad
            '\u2002',  # En space
            '\u2003',  # Em space
            '\u2004',  # Three-per-em space
            '\u2005',  # Four-per-em space
            '\u2006',  # Six-per-em space
            '\u2007',  # Figure space
            '\u2008',  # Punctuation space
            '\u2009',  # Thin space
            '\u200a',  # Hair space
            '\u202f',  # Narrow no-break space
            '\u205f',  # Medium mathematical space
            '\u3000',  # Ideographic space
        }
        return char in special_spaces
    
    def is_similar_char(self, char):
        """Проверяем, является ли символ похожим на стандартный"""
        # Символы, похожие на латинские буквы
        similar_chars = {
            'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x',
            'А': 'A', 'В': 'B', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'О': 'O', 
            'Р': 'P', 'С': 'C', 'Т': 'T', 'У': 'Y', 'Х': 'X'
        }
        return char in similar_chars
    
    def new_file(self):
        """Создаем новый файл"""
        if messagebox.askokcancel("Новый файл", "Очистить текущий документ?"):
            self.text_widget.delete("1.0", tk.END)
            self.clear_highlights()
            self.status_var.set("Новый документ")
    
    def open_file(self):
        """Открываем файл"""
        filename = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_widget.delete("1.0", tk.END)
                    self.text_widget.insert("1.0", content)
                    self.status_var.set(f"Файл открыт: {filename}")
                    if self.auto_highlight.get():
                        self.highlight_all()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    def save_file(self):
        """Сохраняем файл"""
        filename = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Все файлы", "*.*")
            ]
        )
        
        if filename:
            try:
                content = self.text_widget.get("1.0", tk.END)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.status_var.set(f"Файл сохранен: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

def main():
    root = tk.Tk()
    app = NonStandardCharHighlighter(root)
    root.mainloop()

if __name__ == "__main__":
    main()