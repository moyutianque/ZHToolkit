syntax on

set tabstop=4
set shiftwidth=4
set softtabstop=4
set smarttab
set expandtab
set smartindent
set number
set hlsearch
set so=10

" ----- Search settings -------
set ignorecase
" Change to capital awareness mode when type capital letter
set smartcase
" Meet the end, searc will restart from top 
set wrapscan
" key binding , + space for nohl in normal mode
nmap <silent> ,<space> :nohl<CR>
" key binding * for search selected text in visual mode
vmap * y/\V<C-r>"<CR><CR>

set background=dark

if (has("autocmd") && !has("gui_running"))
    augroup colorset
    autocmd!
    let s:white = { "gui": "#ABB2BF", "cterm": "145", "cterm16" : "7" }
    autocmd ColorScheme * call onedark#set_highlight("Normal", { "fg": s:white }) " `bg` will not be styled since there is no `bg` setting
    augroup END
endif


if (empty($TMUX))
  if (has("nvim"))
    "For Neovim 0.1.3 and 0.1.4 <https://github.com/neovim/neovim/pull/2198 >
    let $NVIM_TUI_ENABLE_TRUE_COLOR=1
  endif
  "For Neovim > 0.1.5 and Vim > patch 7.4.1799 <https://github.com/vim/vim/commit/61be73bb0f965a895bfb064ea3e55476ac175162>
  "Based on Vim patch 7.4.1770 (`guicolors` option) <https://github.com/vim/vim/commit/8a633e3427b47286869aa4b96f2bfc1fe65b25cd>
  "<https://github.com/neovim/neovim/wiki/Following-HEAD#20160511>
  if (has("termguicolors"))
    set termguicolors
  endif

endif


let g:onedark_termcolors=256
colorscheme onedark

" file template
au BufNewFile *.py 0r /users/visics/zwang/Documents/workplace/ZHToolkit/header.template
au BufNewFile .gitignore 0r /users/visics/zwang/Documents/workplace/ZHToolkit/gitignore.template

" Keymap
au VimEnter * silent! !xmodmap -e 'clear Lock' -e 'keycode 0x42 = Escape'
au VimLeave * silent! !xmodmap -e 'clear Lock' -e 'keycode 0x42 = Caps_Lock'

" treat _ as whitespace while nevigation
set iskeyword-=_

" Set selection color
hi Visual cterm=bold,reverse guibg=Black guifg=White 
