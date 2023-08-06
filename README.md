# Motivation

I usually use STM32CubeMX while working on some bare-metal embedded projects. It's a powerful tool for STM32 enthusiasts. However, it often generates C code with inadequate formatting, and some of these formats do not align with my preferred style.


Let's take the `app_ble.c` file as an example. It appears that the file permits the utilization of varying formatting styles. This makes the code look suboptimal for readability and I want to fix this.

```C
/* app_ble.c */

static void Adv_Cancel_Req( void )
{
    ...
}

...

static void Switch_OFF_GPIO(){
/* USER CODE BEGIN Switch_OFF_GPIO */

/* USER CODE END Switch_OFF_GPIO */
}

...

void hci_notify_asynch_evt(void* pdata)
{
    ...
}

...

static void BLE_UserEvtRx( void * pPayload )
{
    ...
}
```

After a few searches, [a suggestion](https://community.st.com/t5/stm32-mcu-products/stm32cubemx-source-code-format/m-p/417044/highlight/true#M122359) from an ST Microelectronics employee caught my attention. They recommended the use of an external tool called "[astyle](https://astyle.sourceforge.net/)". This tool serves as a code formatter program designed for the C language. It offers an option to create a configuration file, allowing you to save and share your preferred code formatting style seamlessly.

# Features

- Automatically format the current working file upon saving
- Automatically format all `*.c` and `*.h` files, excluding those within Git-related repositories (submodules, etc.)

# Requirements

In order to use this project, you must have several programs installed.

- [astyle](https://astyle.sourceforge.net/) (>= 3.3)
- [Python](https://www.python.org/downloads/) (>= 3.8)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Astyle](https://marketplace.visualstudio.com/items?itemName=chiehyu.vscode-astyle) (Visual Studio Code Extension)

The project is intended for users who are using Visual Studio Code. If you are using other programs, it might not be suitable for your needs.

# How to use it

1. Add workspace settings to your workspace

```json
"astyle.astylerc": "${workspaceFolder}/.vscode/astylerc",
"editor.defaultFormatter": "chiehyu.vscode-astyle",
"editor.formatOnSave": true
```

> If you prefer not to automatically format the current working file upon saving, change the value of `"editor.formatOnSave"` settings from `true` to `false`.

2. To prevent conflict with `clang-format` formatter, [disable the `clang-format`](https://github.com/welkineins/vscode-astyle#faq).
3. Copy `astylerc` file to your Visual Studio Code configuration folder (`.vscode/`). Alternatively, you can make your own custom settings file. Note that the settings file must be labled as `astylerc`.
4. Copy the `format.py` file to the root of your workspace folder.
   
After following the instructions, the workspace is structured as follows:

```text
Workspace
├─ .vscode              // Visual Studio Code configuration folder 
│  ├─ astylerc          // Astyle code formatting style settings
│  └─ setting.json      // Workspace settings
├─ format.py            // Automatic formatter Python script
├─ Other files          // Other workspace files
...
```

In order to format all `*.c` and `*.h` files, run the `format.py` file.

```bash
python format.py
```
